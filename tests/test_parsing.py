from jarvis.parsing import chunk_text


def test_chunk_text_overlap_and_content():
    text = "A" * 150 + ". " + "B" * 150 + ". " + "C" * 150
    chunks = chunk_text(text, size=200, overlap=30)
    assert len(chunks) >= 2
    assert all(chunks)
