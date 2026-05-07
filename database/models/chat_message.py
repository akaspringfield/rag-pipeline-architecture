from dataclasses import dataclass
from datetime import datetime


@dataclass
class ChatMessage:

    message_id: str

    session_id: str

    role: str

    content: str

    created_at: datetime