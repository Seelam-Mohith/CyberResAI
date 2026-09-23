# CyberResAI

A RAG (Retrieval-Augmented Generation) assistant for cybersecurity incident response, powered by MITRE ATT&CK Atomic Red Team playbooks.

## Overview

CyberResAI ingests the official Atomic Red Team markdown playbooks into a local vector database and answers security questions by retrieving relevant techniques, detection guidance, and atomic test commands from the corpus.

## Tech Stack

- **Language:** Python
- **Embeddings:** Hugging Face `all-MiniLM-L6-v2`
- **Vector Store:** ChromaDB
- **LLM:** Google Gemini (via `GOOGLE_API_KEY`)
- **Framework:** LangChain

## Project Structure

```
CyberResAI/
├── app.py                  # Main application entry point (WIP)
├── ingest.py               # Builds the ChromaDB vector store
├── rag.py                  # Retrieval-augmented generation pipeline (WIP)
├── prompt.py               # Prompt templates (WIP)
├── config.py               # Environment/config loading
├── data/atomics/           # Atomic Red Team markdown playbooks
├── utils/
│   ├── loader.py           # Loads markdown documents
│   ├── splitter.py         # Splits documents into chunks
│   ├── embeddings.py       # Embedding model setup
│   └── retriever.py        # Vector retrieval (WIP)
└── db/                     # ChromaDB persistent store
```

## Setup

1. Clone the repository and install dependencies:

   ```bash
   pip install langchain_chroma langchain_huggingface langchain_community langchain_text_splitters python-dotenv
   ```

2. Create a `.env` file in the project root:

   ```
   GOOGLE_API_KEY=<your-google-api-key>
   ```

3. Build the vector store from the playbooks:

   ```bash
   python ingest.py
   ```

## Usage

```bash
python app.py
```

## Status

Early development. Core ingestion pipeline (load → chunk → embed → index) is functional; the RAG chain, prompt templates, and application entry point are still in progress.

## Disclaimer

This project is for educational and defensive security purposes only. Atomic test playbooks contain simulated adversarial behavior and should only be executed in controlled, authorized environments.