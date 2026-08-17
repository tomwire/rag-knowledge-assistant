"""Document ingestion pipeline: split text into chunks, embed each chunk."""
from app.config import get_settings


# TODO: implement actual ingestion with configurable splitter and embedder.
# Uses character-level splitting as placeholder until a proper text splitter is added.

TEXT_SPLITTER_CHUNK_SIZE = 512
TEXT_SPLITTER_OVERLAP = 64


def split_text(text: str, chunk_size: int = TEXT_SPLITTER_CHUNK_SIZE) -> list[str]:
    """Naive character-based splitter with overlap."""
    if len(text) <= chunk_size:
        return [text]

    chunks = []
    start = 0
    while start < len(text):
        end = min(start + chunk_size, len(text))
        # Try to break on a sentence boundary
        chunk = text[start:end]
        if end < len(text):
            for sep in ["\n\n", "\n. ", ". "]:
                idx = chunk.rfind(sep)
                if idx > chunk_size // 2:
                    chunk = chunk[: idx + len(sep)]
                    end = start + idx + len(sep)
                    break
        chunks.append(chunk)
        start = end - TEXT_SPLITTER_OVERLAP

    return [c for c in chunks if c.strip()]
