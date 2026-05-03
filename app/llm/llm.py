import ollama
from ollama import chat
from app.prompt.prompt_builder import build_prompt
from app.models.llm_models import RAGResponse
from app.models.logs_model import Logs
from app.llm.control_layer import grouding_check
from pathlib import Path
import json


def generate_response(inp : str, n : int = 4):
    prompt, chunks = build_prompt(inp, n)
    response = chat(
        model='mistral:7b',
        messages=[
            {'role' : 'system' , 'content' : prompt},
            {'role' : 'user' , 'content' : inp}]
    )
    
    query = inp
    answer = response.message.content
    prompt_given  = prompt
    model_used = response.model
    chunk_retrieved = chunks
    res = {"query" : query, "answer" : answer, "prompt_given" : prompt_given, "model_used" : model_used, "chunk_retrieved" : chunk_retrieved}
    
    return RAGResponse(**res)

def log_llm_response(inp : RAGResponse, check : bool):
    base_dir = Path(__file__).resolve().parent.parent
    file_path = base_dir / "logger" / "logs.json"
    
    dict = {"query" : inp.query, "answer" : inp.answer, "chunks_dict" : inp.chunk_retrieved , "model" : inp.model_used, "grounding_check" : check}
    res = Logs(**dict)
    json_res = res.model_dump_json()
    with open(file_path,'w') as file:
        json.dump(json_res, file, indent = 4)

    return res


if __name__ == "__main__":
    inp = input("Give your query here : ")
    n = 4
    
    res = generate_response(inp,n)
    check = grouding_check(res)
    if check == False:
        print("I am here")
        res.answer = "I don't have an answer"
    log_llm_response(res , check)
    print(res.answer)
