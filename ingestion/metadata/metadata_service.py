from pathlib import Path


class MetadataService:

    def extract(
        self,
        file_path: str,
        knowledge_base: str,
        knowledge_scope: str,
        owner_type: str,
        tenant_id: str | None = None
    ):

        return {
            "file_name": Path(file_path).name,
            "file_type": Path(file_path).suffix.lower(),
            "knowledge_base": knowledge_base,
            "knowledge_scope": knowledge_scope,
            "owner_type": owner_type,
            "tenant_id": tenant_id
        }