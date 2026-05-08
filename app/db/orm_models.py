from sqlalchemy import Column, Integer, String, Text, DateTime
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

class Base(DeclarativeBase):
    pass

class Session(Base):
    __tablename__ = "sessions"

class Message(Base):
    __tablename__ = "messages"

class ShortTermMemory(Base):
    __tablename__ = "short_term_memory"

class LongTermMemory(Base):
    __tablename__ = "long_term_memory"