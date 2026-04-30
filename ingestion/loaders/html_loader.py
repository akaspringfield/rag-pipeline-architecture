from langchain_community.document_loaders import (
    UnstructuredHTMLLoader
)


class HtmlLoader:

    def __init__(
        self,
        file_path: str
    ):
        self.file_path = file_path

    def load(self):

        return (
            UnstructuredHTMLLoader(
                self.file_path
            ).load()
        )