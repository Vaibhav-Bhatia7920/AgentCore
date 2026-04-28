from pydantic import BaseModel

class Base(BaseModel):
    pass

class ChunkContent(Base):
    text : str
    file_name : str
    chunk_index : int
    similarity_score : float

