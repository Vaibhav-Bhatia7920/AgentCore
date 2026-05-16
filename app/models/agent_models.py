from pydantic import BaseModel
from typing import List

class Base(BaseModel):
    pass


class ToolCall(Base):
    tool_name : str
    arguments : dict

class AgentStep(Base):
    thought : str
    tool_calls : List[ToolCall]
    observation : str

class AgentTrace(Base):
    query : str
    steps : List[AgentStep]
    response : str


