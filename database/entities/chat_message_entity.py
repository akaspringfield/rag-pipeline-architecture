from sqlalchemy import Column, String, DateTime, Text

from database.base import Base


class ChatMessageEntity(Base):

    __tablename__ = "chat_messages"

    message_id = Column(
        String,
        primary_key=True
    )

    session_id = Column(String)

    role = Column(String)

    content = Column(Text)

    created_at = Column(DateTime)