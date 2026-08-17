import uuid
from datetime import datetime

from pydantic import BaseModel, HttpUrl


class DocumentCreate(BaseModel):
    title: str
    source_url: HttpUrl | None = None
    content: str


class DocumentResponse(BaseModel):
    id: str
    title: str
    source_url: str | None = None
    author_id: str
    created_at: datetime

    model_config = {"from_attributes": True}


class ChunkResponse(BaseModel):
    id: str
    document_id: str
    chunk_index: int
    content: str
