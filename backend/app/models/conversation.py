from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from app.database import Base
from datetime import datetime

class Conversation(Base):
    __tablename__ = "conversations"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=True, unique=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    user1_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    user2_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    user1 = relationship("User", foreign_keys=[user1_id])
    user2 = relationship("User", foreign_keys=[user2_id])
    message_conversations = relationship(
        "Message", back_populates="conversation", lazy="select"
    )

    def __repr__(self):
        return f"<Conversation(id={self.id})>"
