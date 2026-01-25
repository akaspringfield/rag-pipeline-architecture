from pydantic import BaseModel


class KnowledgeRequest(BaseModel):
    query: str