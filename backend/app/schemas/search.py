from pydantic import BaseModel


class SearchRequest(BaseModel):
    query: str
    top_k: int = 5
    use_hybrid: bool = True
    min_relevance_score: float = 0.3


class CitationResponse(BaseModel):
    id: str
    document_id: str
    chunk_content: str | None = None
    source_page: int | None = None
    relevance_score: float

    model_config = {"from_attributes": True}


class SearchResponse(BaseModel):
    query: str
    answer: str
    citations: list[CitationResponse]
