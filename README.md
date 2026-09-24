# CyberResAI

A RAG (Retrieval-Augmented Generation) assistant for cybersecurity incident response, powered by MITRE ATT&CK Atomic Red Team playbooks.

## Overview

CyberResAI ingests the official Atomic Red Team markdown playbooks into a local vector database and answers security questions by retrieving relevant techniques, detection guidance, and atomic test commands from the corpus.

## Tech Stack

- **Language:** Python
- **Embeddings:** Hugging Face `all-MiniLM-L6-v2`
- **Vector Store:** ChromaDB
- **LLM:** Groq `openai/gpt-oss-120b` (via `GROQ_API_KEY`)
- **Framework:** LangChain

## Project Structure

```
CyberResAI/
├── app.py                  # Main application entry point (CLI loop)
├── ingest.py               # Builds the ChromaDB vector store
├── rag.py                  # Retrieval-augmented generation pipeline
├── prompt.py               # Prompt templates
├── config.py               # Environment/config loading
├── requirements.txt        # Pinned dependencies
├── data/atomics/           # Atomic Red Team markdown playbooks
├── utils/
│   ├── loader.py           # Loads markdown documents
│   ├── splitter.py         # Splits documents into chunks
│   ├── embeddings.py       # Embedding model setup
│   └── retriever.py        # Vector retrieval
└── db/                     # ChromaDB persistent store (gitignored)
```

## Setup

1. Clone the repository and install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

2. Create a `.env` file in the project root:

   ```
   GROQ_API_KEY=<your-groq-api-key>
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

Functional: ingestion pipeline (load → chunk → embed → index), RAG chain (retrieve → prompt → generate → sources), and CLI entry point are all working. Model: Groq `openai/gpt-oss-120b`.

## Disclaimer

This project is for educational and defensive security purposes only. Atomic test playbooks contain simulated adversarial behavior and should only be executed in controlled, authorized environments.