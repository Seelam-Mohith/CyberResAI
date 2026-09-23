from langchain_chroma import Chroma

from utils.embeddings import embeddings

def get_vector_db():
    return Chroma(
        persist_directory="db",
        embedding_function=embeddings
    )

def get_retriever(k=5):
    vector_db = get_vector_db()
    return vector_db.as_retriever(search_kwargs={"k": k})

if __name__ == "__main__":
    docs = get_retriever().invoke("How does an attacker dump credentials?")

    print(f"Retrieved {len(docs)} documents.\n")

    for i, doc in enumerate(docs, start=1):
        print(f"[{i}] Source: {doc.metadata.get('source')}")
        print("-" * 50)
        print(doc.page_content[:300])
        print()