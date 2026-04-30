from abc import ABC, abstractmethod


class VectorStoreProvider(ABC):

    @abstractmethod
    def add_documents(
        self,
        documents: list
    ):
        pass