from sqlalchemy import JSON, Column, Integer, String, Text, DateTime, Identity, func
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from datetime import datetime

class Base(DeclarativeBase):
    pass

class Session(Base):
    __tablename__ = "sessions"
    id : Mapped[int] = mapped_column(Identity(always=True), primary_key=True)
    chat_conversation: Mapped[list[dict]] = mapped_column(JSON, default=list)

class Message(Base):
    __tablename__ = "messages"
    session_id : Mapped[int] = mapped_column(Integer)
    message_id : Mapped[int] = mapped_column(Identity(always=True), primary_key=True)
    author  : Mapped[str]
    content : Mapped[str]
    timestamp : Mapped[datetime] = mapped_column(DateTime,  server_default=func.now())

class ShortTermMemory(Base):
    __tablename__ = "short_term_memory"
    id : Mapped[int] = mapped_column(Identity(always=True), primary_key=True)

class LongTermMemory(Base):
    __tablename__ = "long_term_memory"
    summaries : Mapped[dict] = mapped_column(JSON, default=dict)
    session_id : Mapped[int] = mapped_column(Integer)