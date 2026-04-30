from pathlib import Path


class DocumentTypeService:

    def detect(
        self,
        file_path: str
    ):

        return (
            Path(file_path)
            .suffix
            .replace(".", "")
            .lower()
        )