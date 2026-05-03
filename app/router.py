from fastapi import FastAPI
from app.pipeline import complete_rag_flow
from app.llm.llm import generate_response
import json
from pathlib import Path

app = FastAPI()

def custom_json_query_response(id : str):

    path = Path(__file__).parent / "logger" / "logs.json" 
    with open(path, "r") as f:
        data = json.load(f)
    
    for item in data:
        if item['id'] == id:
            return item
    
    return {"error" : "id not found"}

def get_tail_traces(limit : int):
    path = Path(__file__).parent / "logger" / "logs.json" 
    with open(path, "r") as f:
        data = json.load(f)
    return data[-limit:]

@app.get("/ask")
async def ask_model(query : str):
    _, result = complete_rag_flow(query)
    return result

@app.get("/health")
async def health_check():
    return {"status" : "ok"}

@app.get("trace/{id}")
async def trace_response(id : str):
    return custom_json_query_response(id)

@app.get("/traces?limit={limit}")
async def get_tail_traces(limit : int):
    return get_tail_traces(limit)
