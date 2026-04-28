from pydantic import BaseModel

class Base(BaseModel):
    pass

class Logs(Base):
    query : str
    answer : str
    chunk_text : str
    chunk_score : float
    model : str