from langchain_community.document_loaders import (
    TextLoader
)


class TxtLoader:

    def __init__(
        self,
        file_path: str
    ):
        self.file_path = file_path

    def load(self):

        return (
            TextLoader(
                self.file_path,
                encoding="utf-8"
            ).load()
        )