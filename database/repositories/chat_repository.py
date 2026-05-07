from database.connection import SessionLocal

from database.entities.chat_session_entity import (
    ChatSessionEntity
)

from database.entities.chat_message_entity import (
    ChatMessageEntity
)


class ChatRepository:

    def create_session(self, session):

        db = SessionLocal()

        try:

            db.add(
                ChatSessionEntity(
                    session_id=session.session_id,
                    user_id=session.user_id,
                    created_at=session.created_at,
                )
            )

            db.commit()

        finally:

            db.close()

    def save_message(self, message):

        db = SessionLocal()

        try:

            db.add(
                ChatMessageEntity(
                    message_id=message.message_id,
                    session_id=message.session_id,
                    role=message.role,
                    content=message.content,
                    created_at=message.created_at,
                )
            )

            db.commit()

        finally:

            db.close()

    def get_messages(
        self,
        session_id: str
    ):

        db = SessionLocal()

        try:

            return (
                db.query(ChatMessageEntity)
                .filter(
                    ChatMessageEntity.session_id
                    == session_id
                )
                .order_by(
                    ChatMessageEntity.created_at
                )
                .all()
            )

        finally:

            db.close()