from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
import datetime
from database import Base



class ChatMessage(Base):
    __tablename__ = "chat_messages"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(String, index=True)
    sender = Column(String)
    message = Column(String)
    timestamp = Column(DateTime, default=datetime.datetime.utcnow)
