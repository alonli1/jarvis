from datetime import date

import httpx

from jarvis.literature import arxiv
from jarvis.literature.arxiv import ArxivSource
from jarvis.literature.search import _source_error

ATOM_FEED = """<?xml version="1.0" encoding="utf-8"?>
<feed xmlns="http://www.w3.org/2005/Atom">
  <entry>
    <id>https://arxiv.org/abs/2608.12345v2</id>
    <updated>2026-08-28T00:00:00Z</updated>
    <published>2026-08-27T00:00:00Z</published>
    <title>Quantum gravity test</title>
    <summary>A useful abstract.</summary>
    <author><name>A. Researcher</name></author>
  </entry>
</feed>
"""


class _Response:
    text = ATOM_FEED

    def raise_for_status(self) -> None:
        pass


class _Client:
    def __init__(self, *args, **kwargs):
        pass

    def __enter__(self):
        return self

    def __exit__(self, *args):
        pass

    def get(self, *args, **kwargs):
        return _Response()


def test_arxiv_source_parses_atom_feed(monkeypatch):
    monkeypatch.setattr(arxiv.httpx, "Client", _Client)

    records = ArxivSource("jarvis-test").search("quantum gravity", date(2026, 8, 1), 10)

    assert len(records) == 1
    assert records[0].arxiv_id == "2608.12345"
    assert records[0].title == "Quantum gravity test"
    assert records[0].authors == ["A. Researcher"]


def test_rate_limit_error_is_concise_and_actionable():
    request = httpx.Request("GET", "https://example.test/search")
    response = httpx.Response(429, request=request)
    error = httpx.HTTPStatusError("rate limited", request=request, response=response)

    assert _source_error(error) == (
        "rate limited (HTTP 429); retry later or configure this source's API key"
    )
