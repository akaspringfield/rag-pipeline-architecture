from pathlib import Path

from ingestion.loaders.pdf_loader import (
    PdfLoader
)

from ingestion.loaders.docx_loader import (
    DocxLoader
)

from ingestion.loaders.txt_loader import (
    TxtLoader
)

from ingestion.loaders.html_loader import (
    HtmlLoader
)


class LoaderFactory:

    @staticmethod
    def get_loader(
        file_path: str
    ):

        extension = (
            Path(file_path)
            .suffix
            .lower()
        )

        if extension == ".pdf":
            return PdfLoader(file_path)

        if extension == ".docx":
            return DocxLoader(file_path)

        if extension == ".txt":
            return TxtLoader(file_path)

        if extension in [
            ".html",
            ".htm"
        ]:
            return HtmlLoader(file_path)

        raise ValueError(
            f"Unsupported file type: "
            f"{extension}"
        )