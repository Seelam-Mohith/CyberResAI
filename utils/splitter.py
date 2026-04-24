from langchain_text_splitters import RecursiveCharacterTextSplitter
from .loader import load_documents

def split_document():
    documents = load_documents()
    
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=800,
        chunk_overlap=150,
        separators=["\n\n", "\n", " ", ""]
    )
    
    chunks = splitter.split_documents(documents)
    
    print(f"Loaded Documents : {len(documents)}")
    print(f"Created Chunks : {len(chunks)}")
    
    
    return chunks

if __name__ == "__main__":

    chunks = split_document()

    print("\nFirst Chunk")
    print("-" * 50)
    print(chunks[0].page_content[:500])