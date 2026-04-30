from langchain_huggingface import (
    HuggingFaceEmbeddings
)

from config.settings import (
    EMBED_MODEL
)


class EmbeddingService:

    _embeddings = None

    def get_embeddings(self):

        if self.__class__._embeddings is None:

            self.__class__._embeddings = (
                HuggingFaceEmbeddings(
                    model_name=EMBED_MODEL
                )
            )

        return self.__class__._embeddings