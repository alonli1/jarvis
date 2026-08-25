from types import SimpleNamespace

from jarvis.index import HybridIndex


class Vector(list):
    def tolist(self):
        return list(self)


class Dense:
    def embed(self, texts):
        yield Vector([0.1, 0.2])


class Sparse:
    def embed(self, texts):
        yield SimpleNamespace(indices=Vector([1]), values=Vector([0.5]))


class Client:
    def collection_exists(self, collection):
        return True

    def query_points(self, **kwargs):
        self.query_filter = kwargs["query_filter"]
        return SimpleNamespace(points=[])


def test_search_filters_tags_inside_qdrant():
    index = object.__new__(HybridIndex)
    index.config = SimpleNamespace(
        retrieval=SimpleNamespace(final_k=10),
        index=SimpleNamespace(dense_limit=30, sparse_limit=30),
    )
    index.client = Client()
    index.dense = Dense()
    index.sparse = Sparse()
    index.collection = "test"

    index.search("gravity", tags=["gravity"])

    conditions = index.client.query_filter.model_dump()["must"]
    assert conditions[0]["key"] == "tags"
    assert conditions[0]["match"]["value"] == "gravity"
