from abc import ABC, abstractmethod


class EmbeddingProvider(ABC):

    @abstractmethod
    def get_embeddings(self):
        pass