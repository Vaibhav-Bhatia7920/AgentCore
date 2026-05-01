from pydantic import BaseModel
from typing import List

class Base(BaseModel):
    pass

class Logs(Base):
    query : str
    answer : str
    chunks_dict : List
    model : str
    grounding_check : bool