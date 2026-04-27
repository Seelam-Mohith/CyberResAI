from langchain_chroma import Chroma

from utils.splitter import split_document
from utils.embeddings import embeddings

def create_vector_db():
    chunks = split_document()

    vector_db = Chroma.from_documents(
        documents=chunks,
        embedding=embeddings,
        persist_directory="db"
    )

    print(f"Stored {len(chunks)} chunks in the ChromaDB.")

if __name__ == "__main__":
    create_vector_db()
