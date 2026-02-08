# query_processing/classifier.py

from enum import Enum


class QueryType(str, Enum):

    KNOWLEDGE = "knowledge"
    UNKNOWN = "unknown"


def classify_query(query: str) -> QueryType:

    return QueryType.KNOWLEDGE