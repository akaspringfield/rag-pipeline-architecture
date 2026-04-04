from dataclasses import dataclass


@dataclass
class SourceResponse:

    answer: str

    sources: list[str]