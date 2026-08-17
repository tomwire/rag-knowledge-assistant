from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.database import get_db
from app.models.document import Document, Chunk
from app.schemas.documents import DocumentCreate, DocumentResponse, ChunkResponse

router = APIRouter(prefix="/documents", tags=["documents"])


@router.post("/", response_model=DocumentResponse)
async def create_document(
    payload: DocumentCreate,
    db: AsyncSession = Depends(get_db),
):
    doc = Document(title=payload.title, source_url=str(payload.source_url) if payload.source_url else None, content=payload.content, author_id="placeholder-user-id")
    db.add(doc)
    await db.commit()
    await db.refresh(doc)
    return DocumentResponse(
        id=str(doc.id),
        title=doc.title,
        source_url=doc.source_url,
        author_id=str(doc.author_id),
        created_at=doc.created_at,
    )


@router.get("/", response_model=list[DocumentResponse])
async def list_documents(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Document).order_by(Document.created_at.desc()))
    docs = result.scalars().all()
    return [
        DocumentResponse(
            id=str(d.id), title=d.title, source_url=d.source_url, author_id=str(d.author_id), created_at=d.created_at,
        )
        for d in docs
    ]


@router.get("/{doc_id}/chunks", response_model=list[ChunkResponse])
async def get_chunks(doc_id: str, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Chunk).where(Chunk.document_id == doc_id).order_by(Chunk.chunk_index))
    chunks = result.scalars().all()
    return [
        ChunkResponse(id=str(c.id), document_id=str(c.document_id), chunk_index=c.chunk_index, content=c.content)
        for c in chunks
    ]


@router.delete("/{doc_id}", status_code=204)
async def delete_document(doc_id: str, db: AsyncSession = Depends(get_db)):
    doc = await db.get(Document, doc_id)
    if not doc:
        raise HTTPException(status_code=404, detail="Document not found")
    await db.delete(doc)
    await db.commit()
