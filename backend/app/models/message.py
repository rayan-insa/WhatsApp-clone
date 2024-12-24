from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from app.database import Base
from datetime import datetime


class Message(Base):
    __tablename__ = "messages"

    id = Column(Integer, primary_key=True, index=True)
    content = Column(String(500), nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow)
    sender_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    conversation_id = Column(Integer, ForeignKey("conversations.id"), nullable=True)
    groupchat_id = Column(Integer, ForeignKey("groupchats.id"), nullable=True)
    
    sender = relationship("User", backref="sent_messages")
    conversation = relationship(
        "Conversation", back_populates="message_conversations", uselist=False
    )
    groupchat = relationship(
        "GroupChat", back_populates="message_groupchats", uselist=False
    )

    def __repr__(self):
        return f"<Message(id={self.id}, content={self.content[:20]})>"
