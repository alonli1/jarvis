from __future__ import annotations

from pathlib import Path
import uuid

from fastembed import SparseTextEmbedding, TextEmbedding
from qdrant_client import QdrantClient, models

from .config import Config
from .models import Chunk, SearchHit, Visibility
from .parsing import discover_documents, iter_document_chunks


class HybridIndex:
    def __init__(self, config: Config):
        self.config = config
        if config.index.mode == "server":
            self.client = QdrantClient(url=config.index.url)
        else:
            storage = config.root / config.index.path
            storage.parent.mkdir(parents=True, exist_ok=True)
            self.client = QdrantClient(path=str(storage))
        self.dense = TextEmbedding(model_name=config.index.dense_model)
        self.sparse = SparseTextEmbedding(model_name=config.index.sparse_model)
        self.collection = config.index.collection

    def _ensure_collection(self) -> None:
        if self.client.collection_exists(self.collection):
            return
        probe = next(iter(self.dense.embed(["physics"])))
        dim = len(probe)
        self.client.create_collection(
            collection_name=self.collection,
            vectors_config={
                "dense": models.VectorParams(size=dim, distance=models.Distance.COSINE),
            },
            sparse_vectors_config={
                "sparse": models.SparseVectorParams(),
            },
        )

    @staticmethod
    def _point_id(chunk_id: str) -> str:
        return str(uuid.uuid5(uuid.NAMESPACE_URL, f"jarvis:{chunk_id}"))

    def delete_source(self, source_path: str) -> None:
        self._ensure_collection()
        self.client.delete(
            collection_name=self.collection,
            points_selector=models.FilterSelector(
                filter=models.Filter(
                    must=[models.FieldCondition(key="source_path", match=models.MatchValue(value=source_path))]
                )
            ),
        )

    def upsert_chunks(self, chunks: list[Chunk]) -> None:
        if not chunks:
            return
        self._ensure_collection()
        texts = [c.text for c in chunks]
        dense_vectors = list(self.dense.embed(texts))
        sparse_vectors = list(self.sparse.embed(texts))
        points = []
        for chunk, dv, sv in zip(chunks, dense_vectors, sparse_vectors, strict=True):
            points.append(
                models.PointStruct(
                    id=self._point_id(chunk.id),
                    vector={
                        "dense": dv.tolist(),
                        "sparse": models.SparseVector(
                            indices=sv.indices.tolist(), values=sv.values.tolist()
                        ),
                    },
                    payload=chunk.model_dump(),
                )
            )
        self.client.upsert(collection_name=self.collection, points=points, wait=True)

    def ingest(self, target: Path) -> tuple[int, int]:
        docs = discover_documents(target)
        total_chunks = 0
        for doc in docs:
            rel = str(doc.resolve().relative_to(self.config.root.resolve()))
            self.delete_source(rel)
            chunks = list(
                iter_document_chunks(
                    doc,
                    repo_root=self.config.root,
                    chunk_chars=self.config.retrieval.chunk_chars,
                    overlap=self.config.retrieval.chunk_overlap,
                )
            )
            self.upsert_chunks(chunks)
            total_chunks += len(chunks)
        return len(docs), total_chunks

    def search(self, query: str, k: int | None = None, max_visibility: str = "public") -> list[SearchHit]:
        self._ensure_collection()
        k = k or self.config.retrieval.final_k
        dense_query = next(iter(self.dense.embed([query])))
        sparse_query = next(iter(self.sparse.embed([query])))
        result = self.client.query_points(
            collection_name=self.collection,
            prefetch=[
                models.Prefetch(
                    query=dense_query.tolist(),
                    using="dense",
                    limit=self.config.index.dense_limit,
                ),
                models.Prefetch(
                    query=models.SparseVector(
                        indices=sparse_query.indices.tolist(), values=sparse_query.values.tolist()
                    ),
                    using="sparse",
                    limit=self.config.index.sparse_limit,
                ),
            ],
            query=models.RrfQuery(rrf=models.Rrf()),
            limit=max(k * 3, k),
            with_payload=True,
        )
        max_level = Visibility.parse(max_visibility)
        hits: list[SearchHit] = []
        for p in result.points:
            payload = dict(p.payload or {})
            chunk = Chunk.model_validate(payload)
            if Visibility.parse(chunk.visibility) <= max_level:
                hits.append(SearchHit(chunk=chunk, score=float(p.score)))
            if len(hits) >= k:
                break
        return hits
