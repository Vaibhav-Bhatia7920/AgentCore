from app.llm.llm import generate_response
from app.llm.control_layer import llm_grounding_check
from app.llm.llm import log_llm_response
from app.llm.llm import log_llm_response2
from app.llm.trace import log_tracing
from app.llm.mock_llm import mock_generate_response
from app.db.orm_models import Session, Message, ShortTermMemory, LongTermMemory, Base
from app.db.db_ops import init_db, get_db_session, initiate_session, add_message
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import json
from pathlib import Path

engine = create_engine('sqlite:///agent_core.db')
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
    id = initiate_session("New session initiated.")
    return id

def session_flow(session_id: int, query : str, number : int = 4):
    id = session_id
    while True:
        res = generate_response(query, number, session_id=id)
        print(f"Agent's response : {res.answer}")
        add_message(id, "user", query, None)
        add_message(id, "agent", res.answer, None)
        query = input("Enter your query here if you want to continue the session, else type 'exit' to end the session : ")
        if query.lower() == "exit":
            break
    
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

    
