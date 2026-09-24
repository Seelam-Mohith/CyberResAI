from typing import Any, List

from langchain_core.documents import Document
from langchain_core.retrievers import BaseRetriever
from langchain_chroma import Chroma

from utils.embeddings import embeddings
from utils.query import optimize_query

NOISE_SOURCE_SUBSTRINGS = ("indexes-markdown", "matrices")

def _is_noise(source):
    if not source:
        return True
    normalized = source.replace("/", "\\").lower()
    return any(part in normalized for part in NOISE_SOURCE_SUBSTRINGS)

class _FilteredRetriever(BaseRetriever):
    base_retriever: Any
    k: int = 10

    def _get_relevant_documents(self, query: str, *, run_manager=None) -> List[Document]:
        docs = self.base_retriever.invoke(query)
        kept = [d for d in docs if not _is_noise(d.metadata.get("source", ""))]
        return kept[: self.k]

def get_vector_db():
    return Chroma(
        persist_directory="db",
        embedding_function=embeddings
    )

def get_retriever(k=10):
    vector_db = get_vector_db()
    base_retriever = vector_db.as_retriever(search_kwargs={"k": k * 3})
    return _FilteredRetriever(base_retriever=base_retriever, k=k)

if __name__ == "__main__":
    docs = get_retriever().invoke(optimize_query("How does an attacker dump credentials?"))

    print(f"Retrieved {len(docs)} documents.\n")

    for i, doc in enumerate(docs, start=1):
        print(f"[{i}] Source: {doc.metadata.get('source')}")
        print("-" * 50)
        print(doc.page_content[:300])
        print()