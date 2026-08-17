"""Hybrid search combining dense (vector) and sparse (BM25-style) retrieval."""
import math
from collections import defaultdict

from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.database import get_db
from app.models.document import Chunk


# TODO: Replace with actual pgvector cosine similarity + BM25 scoring once OpenAI API is wired.

TOP_K_DEFAULT = 10


async def hybrid_search(
    db: AsyncSession,
    query_vector: list[float],
    query_text: str,
    top_k: int = TOP_K_DEFAULT,
) -> list[dict]:
    """Return the most relevant chunks for a given query.

    Falls back to a keyword-match heuristic since vector similarity isn't wired yet.
    """
    result = await db.execute(
        select(Chunk).order_by(Chunk.created_at.desc()).limit(top_k * 2)
    )
    candidates = list(result.scalars().all())

    scored = []
    for chunk in candidates:
        score = _keyword_score(chunk.content, query_text)
        if score > 0:
            scored.append({"chunk": chunk, "score": score})

    scored.sort(key=lambda x: x["score"], reverse=True)
    return scored[:top_k]


def _keyword_score(content: str, query: str) -> float:
    """Simple term-frequency scoring."""
    terms = query.lower().split()
    text_lower = content.lower()
    score = 0.0
    for term in terms:
        if term in text_lower:
            count = text_lower.count(term)
            score += count / (len(text_lower.split()) + 1e-9)
    return score
