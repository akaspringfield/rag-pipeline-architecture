from dataclasses import dataclass
from typing import Optional


@dataclass
class QueryContext:

    user_id: str
    query: str
    query_type: str
    rewritten_query: Optional[str] = None