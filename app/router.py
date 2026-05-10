from fastapi import FastAPI
from app.pipeline import complete_rag_flow
from app.llm.llm import generate_response
from app.pipeline import session_flow, get_new_session_id
from app.db.db_ops import query_session_conversation
import json
from collections import deque
from pathlib import Path
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

app = FastAPI()

def custom_json_query_response(id : str):

    path = Path(__file__).parent / "logger" / "logs.jsonl" 
    data = []
    with open(path, "r", encoding='utf-8') as f:
        for line in f:
            line_dict = json.loads(line)
            data.append(json.loads(line_dict))
    
    print(data)
    for item in data:
        if item['id'] == id:
            return item
    
    return {"error" : "id not found"}

def get_tail_traces1(limit : int):
    path = Path(__file__).parent / "logger" / "logs.jsonl" 
    with open(path, "r", encoding='utf-8') as f:
        last_lines = deque(f, maxlen=limit)
    data =[json.loads(line) for line in last_lines]
    return data

@app.get("/ask")
async def ask_model(query : str, session_id : int = None):
    if session_id == None:
        id = session_flow(get_new_session_id(), query)
    else:
        id = session_flow(session_id, query)
    convo = query_session_conversation(id)
    print(convo)
        # You can implement session-based logic here if needed
    
    return {"session_id" : id}
    # _, result = complete_rag_flow(query)
    # return result

@app.get("/health")
async def health_check():
    return {"status" : "ok"}

@app.get("/trace/{id}")
async def trace_response(id : str):
    return custom_json_query_response(id)

@app.get("/traces")
async def get_tail_traces(limit : int = 2):
    return get_tail_traces1(limit)
