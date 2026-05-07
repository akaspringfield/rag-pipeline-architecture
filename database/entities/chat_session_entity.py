from sqlalchemy import Column, String, DateTime

from database.base import Base


class ChatSessionEntity(Base):

    __tablename__ = "chat_sessions"

    session_id = Column(
        String,
        primary_key=True
    )

    user_id = Column(
        String,
        nullable=True
    )

    created_at = Column(DateTime)