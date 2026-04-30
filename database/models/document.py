from dataclasses import dataclass
from datetime import datetime


@dataclass
class Document:

    document_id: str

    knowledge_base: str

    knowledge_scope: str

    owner_type: str

    tenant_id: str | None

    document_type: str

    source_file: str

    file_hash: str

    status: str

    created_at: datetime