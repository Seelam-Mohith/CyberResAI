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
streamlit run app_ui.py
```

For the terminal CLI:

```bash
python app.py
```

## Deploy to Streamlit Community Cloud

The `db/` vector store is committed so the cloud app starts instantly.

1. Push this repository to GitHub.
2. Go to [share.streamlit.io](https://share.streamlit.io) → **Create app** → "Yup, I have an app".
3. Enter your repo, branch, and set **Main file path** to `main.py`.
4. Open **Advanced settings**:
   - **Python version:** `3.12` — **required.** Community Cloud recently defaults to Python 3.14, which has no `pyarrow` wheels; the build then tries to compile Arrow from source and fails on a missing `cmake`.
   - **Secrets:** paste
     ```
     GROQ_API_KEY = "<your-groq-api-key>"
     ```
5. Click **Deploy**.

> **Already deployed with the wrong Python?** The version can't be changed after deploy. Delete the app and redeploy, selecting `3.12` in Advanced settings this time. (`pyarrow` ships wheels for 3.12/3.13 only; Python 3.14 always fails the build.)

Notes:
- First cold start downloads the Hugging Face embedding model (~90 MB) and can take about a minute; later loads are faster.
- If the app fails to start with a `libgomp` error, add a `packages.txt` at the repo root containing `libgomp1`.

## Status

Functional: ingestion pipeline (load → chunk → embed → index), RAG chain (retrieve → prompt → generate → sources), and CLI entry point are all working. Model: Groq `openai/gpt-oss-120b`.

## Disclaimer

This project is for educational and defensive security purposes only. Atomic test playbooks contain simulated adversarial behavior and should only be executed in controlled, authorized environments.