from app.llm.llm import generate_response
from app.llm.control_layer import llm_grounding_check
from app.llm.llm import log_llm_response
from app.llm.llm import log_llm_response2
from app.llm.trace import log_tracing
from app.llm.mock_llm import mock_generate_response
from app.db.orm_models import Session, Message, ShortTermMemory, LongTermMemory, Base
from app.db.db_ops import init_db, get_db_session, initiate_session, add_message, update_long_term_memory, initiate_long_term_memory
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import json
from pathlib import Path
import os
from dotenv import load_dotenv

load_dotenv()  # Load environment variables from .env file


db_password = os.getenv("POSTGRES_PASSWORD")
db_user = "postgres"
db_name = "agentcore_db"
# Default Postgres port is 5432
db_host = "localhost"

engine = create_engine(f'postgresql://{db_user}:{db_password}@{db_host}/{db_name}')
SessionLocal = sessionmaker(bind=engine)

def complete_rag_flow(query : str, number : int = 4):
   
    res = generate_response(query, number)
    check = llm_grounding_check(res)
    if check == False:
        print("I am here")
        res.answer = "I don't have an answer"
    res2 = log_llm_response(res , check)
    log_tracing(res2)
    return res2, res
    
def complete_rag_flow_mock(query : str, number : int = 4):

    res = mock_generate_response(query, number)
    check = llm_grounding_check(res)
    if check == False:
        print("I am here")
        res.answer = "I don't have an answer"
    res2 = log_llm_response(res , check)
    log_tracing(res2)
    return res2, res

def complete_rag_flow_golden_dataset(query : str, number : int = 4):

    res = generate_response(query, number)
    check = llm_grounding_check(res)
    if check == False:
        print("I am here")
        res.answer = "I don't have an answer"
    res2 = log_llm_response2(res , check)
    return res2, res

def get_new_session_id():
    id = initiate_session([{"author" : "system", "content" : "This is the start of the session. The assistant is here to help you with your queries."}])
    return id

def session_flow(query : str, number : int = 4, session_id : int = None):
    id = session_id or get_new_session_id()
    initiate_long_term_memory(id, {"session_id" : id, "summaries" : {}})
    while True:
        res = generate_response(query, number, session_id=id)
        print(f"Agent's response : {res.answer}")
        add_message(id, "user", query, None)
        add_message(id, "agent", res.answer, None)
        query = input("Enter your query here if you want to continue the session, else type 'exit' to end the session : ")
        if query.lower() == "exit":
            break
    
    update_long_term_memory(id)
    return id


if __name__ == "__main__":
    n = 4
    session = SessionLocal()
    # file = Path(__file__).resolve().parent.parent / "tests" / "golden_test.jsonl"
    # with open(file, 'r') as f:
    #     data = json.load(f)
    #     for item in data:
    #         inp = item['question']
    #         _ , _ = complete_rag_flow_golden_dataset(inp, n)
    inp = input("Enter your query here : ")
    id = session_flow(inp, n)
    s1 = session.query(Session).filter(Session.id == id).first()
    print(s1.chat_conversation)

    
