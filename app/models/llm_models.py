from pydantic import BaseModel
from typing import List
from app.models.chunk_models import ChunkContent

class Base(BaseModel):
    pass

class RAGResponse(Base):
    query : str
    answer : str
    prompt_given : str
    model_used : str
    chunk_retrieved : List[ChunkContent]