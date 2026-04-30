from dataclasses import dataclass
from datetime import datetime


@dataclass
class DocumentChunk:

    chunk_id: str

    document_id: str

    chunk_index: int

    knowledge_base: str

    knowledge_scope: str

    owner_type: str

    tenant_id: str | None

    content: str

    source: str

    created_at: datetime