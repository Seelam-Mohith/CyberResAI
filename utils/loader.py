from langchain_community.document_loaders import DirectoryLoader, TextLoader

def load_documents(data_path="data/atomics"):
    loader = DirectoryLoader(
        path=data_path,
        glob="**./*.md",
        loader_cls=TextLoader,
        show_progress=True,
        silent_errors=True
    )
    documents = loader.load()

    print(f"Loaded {len(documents)} documents.")

    return documents


if __name__ == "__main__":
    docs = load_documents()

    print("\nFirst Document")
    print("-" * 50)
    print("Source:", docs[0].metadata["source"])
    print(docs[0].page_content[:500])