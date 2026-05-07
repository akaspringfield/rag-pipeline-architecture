from dataclasses import dataclass
from datetime import datetime


@dataclass
class ChatSession:

    session_id: str

    user_id: str | None

    created_at: datetime