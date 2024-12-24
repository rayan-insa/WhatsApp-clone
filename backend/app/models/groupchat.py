from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Table
from sqlalchemy.orm import relationship
from app.database import Base
from datetime import datetime

# Association table for users and group chats
group_members = Table(
    "group_members",
    Base.metadata,
    Column("user_id", Integer, ForeignKey("users.id")),
    Column("group_id", Integer, ForeignKey("groupchats.id")),
)


class GroupChat(Base):
    __tablename__ = "groupchats"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False, unique=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    admin_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    admin = relationship("User", backref="administered_groups")
    members = relationship(
        "User",
        secondary=group_members,
        backref="group_chats",
        cascade="all",
    )
    message_groupchats = relationship(
        "Message", back_populates="groupchat", lazy="select"
    )

    def __repr__(self):
        return f"<GroupChat(id={self.id}, name={self.name})>"
