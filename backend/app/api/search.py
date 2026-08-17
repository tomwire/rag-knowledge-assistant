from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.database import get_db
from app.schemas.search import SearchRequest, SearchResponse, CitationResponse

router = APIRouter(prefix="/search", tags=["search"])


@router.post("/", response_model=SearchResponse)
async def search(req: SearchRequest, db: AsyncSession = Depends(get_db)):
    """Return an LLM-generated answer with citations from the knowledge base.

    TODO: wire up OpenAI embeddings + pgvector similarity search + BM25 fallback.
    Returns a placeholder until vector search is fully implemented.
    """
    raise HTTPException(
        status_code=501,
        detail={
            "query": req.query,
            "answer": f"No results found for: {req.query}",
            "citations": [],
        },
    )
