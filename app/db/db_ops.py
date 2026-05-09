from app.db.orm_models import Session, Message, ShortTermMemory, LongTermMemory, Base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker



engine = create_engine('sqlite:///agent_core.db')
SessionLocal = sessionmaker(bind=engine)

def init_db():
    Base.metadata.create_all(bind=engine)

def get_db_session(session_id: int):
   
    db_session = SessionLocal()
    return db_session.query(Session).filter(Session.id == session_id).first()


def initiate_session(chat_conversation: str):
    db_session = SessionLocal()
    session = Session(chat_conversation=chat_conversation)
    db_session.add(session)
    db_session.commit()
    db_session.refresh(session)
    db_session.close()
    return session.id

def add_message(session_id: int, author: str, content: str, timestamp):
    db_session = SessionLocal()
    message = Message(session_id = session_id,author=author, content=content, timestamp=timestamp)
    session = db_session.query(Session).filter(Session.id == session_id).first()
    if session:
        session.chat_conversation += f"\n{author}: {content}"
    db_session.add(message)
    db_session.commit()
    db_session.close()

if __name__ == "__main__":
    init_db()
    print("Database initialized.")
    id = initiate_session("Hello, this is a new session.")
    print(f"Session initiated with ID: {id}")
    add_message(id, "user", "Hello, how are you?", None)
    print("Message added to the database.")
    session = get_db_session(id)

    print(session.chat_conversation)