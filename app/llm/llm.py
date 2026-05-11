import ollama
from ollama import chat
from app.prompt.prompt_builder import build_prompt
from app.models.llm_models import RAGResponse
from app.models.logs_model import Logs
from app.llm.control_layer import grouding_check
from pathlib import Path
from datetime import datetime, timezone
from openai import OpenAI
import os
from dotenv import load_dotenv
import json

load_dotenv()
openai_api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI()

def make_openai_api_call(inp : str):
    response = client.chat.completions.create(
        model="gpt-5.5-mini",
        messages=[
            {"role" : "system" , "content" : "You are a helpful assistant."},
            {"role" : "user" , "content" : inp}
        ]
    )
    return response.choices[0].message.content

def generate_response(inp : str, n : int = 4, session_id : int = None):
    prompt, chunks = build_prompt(inp, n, session_id)
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
    file_path = base_dir / "logger" / "logs.jsonl"
    
    timestamp = datetime.now(timezone.utc).isoformat(timespec='milliseconds')
    dict = {"query" : inp.query, "answer" : inp.answer, "chunks_dict" : inp.chunk_retrieved , "model" : inp.model_used, "grounding_check" : check, "timestamp" : timestamp, "id" : timestamp}
    res = Logs(**dict)
    json_res = res.model_dump_json()
    with open(file_path,'a') as file:
        file.write(json.dumps(json_res) + "\n")

    return res

def log_llm_response2(inp : RAGResponse, check : bool):
    base_dir = Path(__file__).resolve().parent.parent
    file_path = base_dir / "logger" / "golden_dataset_logs.jsonl"
    
    timestamp = datetime.now(timezone.utc).isoformat(timespec='milliseconds')
    dict = {"query" : inp.query, "answer" : inp.answer, "chunks_dict" : inp.chunk_retrieved , "model" : inp.model_used, "grounding_check" : check, "timestamp" : timestamp, "id" : timestamp}
    res = Logs(**dict)
    json_res = res.model_dump_json()
    with open(file_path,'a') as file:
        file.write(json.dumps(json_res) + "\n")

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
