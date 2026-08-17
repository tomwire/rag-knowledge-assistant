"""OpenAI embedding service wrapper."""
from openai import AsyncOpenAI

from app.config import get_settings


settings = get_settings()

_client: AsyncOpenAI | None = None


def _get_client() -> AsyncOpenAI:
    global _client
    if _client is None:
        _client = AsyncOpenAI(api_key=settings.OPENAI_API_KEY)
    return _client


async def embed(texts: list[str], model: str | None = None) -> list[list[float]]:
    """Embed a batch of texts and return the vectors."""
    client = _get_client()
    result = await client.embeddings.create(input=texts, model=model or settings.EMBEDDING_MODEL)
    return [item.embedding for item in result.data]


async def embed_single(text: str, model: str | None = None) -> list[float]:
    vecs = await embed([text], model)
    return vecs[0]
