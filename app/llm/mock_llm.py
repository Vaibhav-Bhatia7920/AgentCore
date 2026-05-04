from unittest.mock import MagicMock
from app.models.llm_models import RAGResponse
from app.prompt.prompt_builder import build_prompt

def mock_generate_response(query: str, n: int = 4):
    
    prompt, chunks = build_prompt(query, n)
    mock_llm = MagicMock()

    mock_llm.invoke.return_value = "This is a mock response to the query: " + query

    response = mock_llm.invoke(query)
    answer = response
    prompt_given  = prompt
    model_used = "mock-llm"
    chunk_retrieved = chunks
    res = {"query" : query, "answer" : answer, "prompt_given" : prompt_given, "model_used" : model_used, "chunk_retrieved" : chunk_retrieved}
    
    return RAGResponse(**res)
    