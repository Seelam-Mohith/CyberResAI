from chromadb.utils.embedding_functions import DefaultEmbeddingFunction


class _ONNXEmbeddings:
    def __init__(self):
        self._fn = DefaultEmbeddingFunction()
        self.model_name = "all-MiniLM-L6-v2"

    def embed_documents(self, texts):
        return self._fn(texts)

    def embed_query(self, text):
        return self._fn([text])[0]


embeddings = _ONNXEmbeddings()