import json

from app.db.orm_models import Session, Message, ShortTermMemory, LongTermMemory, Base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.llm.llm_ops import make_ollama_call
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

def init_db():
    Base.metadata.create_all(bind=engine)

def get_db_session(session_id: int):
   
    db_session = SessionLocal()
    return db_session.query(Session).filter(Session.id == session_id).first()


def initiate_session(chat_conversation: list[dict]):
    db_session = SessionLocal()
    session = Session(chat_conversation=chat_conversation)
    db_session.add(session)
    db_session.commit()
    db_session.refresh(session)
    db_session.close()
    return session.id

def initiate_long_term_memory(session_id: int, summaries: dict):
    db_session = SessionLocal()
    memory = LongTermMemory(summaries=summaries, session_id=session_id)
    db_session.add(memory)
    db_session.commit()
    db_session.close()

def make_conversation_string(conversation : list[dict]):
    convo_str = ""
    for message in conversation:
        convo_str += f"{message['author']} : {message['content']} \n"
    return convo_str

def add_message(session_id: int, author: str, content: str, timestamp):
    db_session = SessionLocal()
    message = Message(session_id = session_id,author=author, content=content, timestamp=timestamp)
    session = db_session.query(Session).filter(Session.id == session_id).first()
    if session:
        session.chat_conversation.append({"author": author, "content": content})
    db_session.add(message)
    db_session.commit()
    db_session.close()

def get_last_n_messages(session_id: int, n: int):
    db_session = SessionLocal()
    session = db_session.query(Session).filter(Session.id == session_id).first()
    db_session.close()
    print("Session , chat_conversation: ", session.chat_conversation)
    if session:
        convo = ""
        for message in session.chat_conversation[-n:]:
            print("Message : ", message)
            convo += f"{message['author']} : {message['content']} \n"
        return convo
    else:
        return None

def extract_important_info(conversation : list[dict]):
    convo_str = make_conversation_string(conversation)
    prompt = f"Extract important information from the following conversation : {convo_str} \n Important information should be in the form of key value pairs, where key is the topic and value is the information related to that topic. If there is no important information, return an empty dictionary."
    response = make_ollama_call(prompt)
    try:
        info_dict = json.loads(response)
    except:
        info_dict = {}
    return info_dict

def update_long_term_memory(session_id: int):
    db_session = SessionLocal()
    session = db_session.query(Session).filter(Session.id == session_id).first()
    if session:
        info_dict = extract_important_info(session.chat_conversation)
    if db_session.query(LongTermMemory).filter(LongTermMemory.session_id == session_id).first():
        memory = db_session.query(LongTermMemory).filter(LongTermMemory.session_id == session_id).first()
        memory.summaries = info_dict
    else:   
        memory = LongTermMemory(summaries=info_dict, session_id=session_id)
    db_session.add(memory)
    db_session.commit()
    db_session.close()

def get_long_term_memory():
    db_session = SessionLocal()
    memories = db_session.query(LongTermMemory).all()
    facts = ""
    for memory in memories:
        for key, value in memory.summaries.items():
            facts += f"{key}: {value}\n"
    db_session.close()
    return facts

def query_session_conversation(session_id: int):
    db_session = SessionLocal()
    session = db_session.query(Session).filter(Session.id == session_id).first()
    if session:
        return session.chat_conversation
    else:
        return None
## For short term memory we can just make a queue of sessions, for long term memory summariries of important sessions.
if __name__ == "__main__":
    init_db()
    print("Database initialized.")
    id = initiate_session([{"author": "user", "content": "Hello, this is a new session."}])
    print(f"Session initiated with ID: {id}")
    add_message(id, "user", "Hello, how are you?", None)
    print("Message added to the database.")
    session = get_db_session(id)

    print(session.chat_conversation)