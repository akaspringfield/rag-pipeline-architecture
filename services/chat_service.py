from uuid import uuid4
from datetime import datetime

from database.models.chat_session import ChatSession
from database.models.chat_message import ChatMessage

from database.repositories.chat_repository import (
    ChatRepository
)


class ChatService:

    def __init__(self):

        self.repository = ChatRepository()

    def create_session(
        self,
        user_id=None,
    ):

        session = ChatSession(
            session_id=str(uuid4()),
            user_id=user_id,
            created_at=datetime.utcnow(),
        )

        self.repository.create_session(session)

        return session

    def save_message(
        self,
        session_id,
        role,
        content,
    ):

        message = ChatMessage(
            message_id=str(uuid4()),
            session_id=session_id,
            role=role,
            content=content,
            created_at=datetime.utcnow(),
        )

        self.repository.save_message(message)

        return message

    def get_messages(
        self,
        session_id,
    ):

        return self.repository.get_messages(
            session_id
        )