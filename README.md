# INFO 5940 — Retrieval-Augmented Generation (RAG) Application

Welcome to the **INFO 5940 Assignment 1** repository.  
This project implements a **Retrieval-Augmented Generation (RAG)** system using **Streamlit**, **LangChain**, **Chroma**, and **OpenAI**.  
It allows users to upload `.txt` and `.pdf` files and interact with their content through a conversational chat interface.

## Getting Started

### Step 1 – Open Your Forked Repository
1. Fork the class repository to your GitHub account.
2. Click the green **Code** button → **Codespaces** tab → **Create Codespace**.
3. Wait for the environment to finish building (Python 3.11.13).

### Step 2 – Verify Your Environment
1. Ensure the **Python 3.11** kernel is selected.
2. The `.devcontainer` will automatically install required dependencies.

### Step 3 – Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 4 – Run the Streamlit App

In the terminal, run:

```bash
streamlit run chat_with_pdf.py
```

When prompted, click **Open in Browser** to view the app interface.

## Application Overview

### What the Application Does

1. Upload one or more `.txt` and `.pdf` files.
2. Extract and chunk text automatically for efficient retrieval.
3. Generate vector embeddings using OpenAI's `text-embedding-3-large` model.
4. Store and retrieve document chunks from a Chroma vector database.
5. Ask questions through a chat interface powered by GPT-4o.
6. Receive concise, context-grounded answers drawn directly from the uploaded materials.

### Application Features

- **Multi-file Upload**: supports `.txt`, `.pdf`, and `.md` documents.
- **Automatic PDF Parsing**: extracts text from PDF pages using PyPDF.
- **Document Chunking**: splits text into ~200-character chunks (no overlap).
- **Vector Embeddings**: uses OpenAI `text-embedding-3-large` model.
- **Semantic Retrieval**: performs similarity search with Chroma (k = 20).
- **Conversational Chat**: GPT-4o provides concise, grounded answers.
- **Multi-Turn Memory**: chat history stored in `st.session_state`.
- **Streaming Responses**: messages appear in real time in the UI.

## Environment Variables

The following variables are pre-configured in `.devcontainer.json`:

```
OPENAI_API_KEY=<your key>
OPENAI_BASE_URL=https://api.ai.it.cornell.edu
```

If running locally, export them manually before launching the app:

```bash
export OPENAI_API_KEY="your_key_here"
export OPENAI_BASE_URL="https://api.ai.it.cornell.edu"
```

## Configuration Changes

### Updates Made to the Provided Codespace Setup

**Added dependencies to `requirements.txt`:**

```
chromadb>=0.5.5          # Vector database for storing embeddings
langchain-text-splitters # For document chunking
pypdf                    # For PDF reading and extraction
```

- **`chromadb>=0.5.5`** – installs Chroma (v 0.5.5 or higher) for vector storage and retrieval.
- **`langchain-text-splitters`** – provides utilities to split large documents into smaller chunks for RAG.
- **`pypdf`** – adds PDF parsing capability to handle uploaded `.pdf` files.

**Added Python import in main script:**

```python
from pypdf import PdfReader  # PDF reader
```

**Encoded API Key securely inside Codespace:**

```
${localEnv:OPENAI_API_KEY}
```

Stores the OpenAI API key as a secret variable so it is not exposed in source control.

**Optional reinstall command used to fix dependency conflicts:**

```bash
pip install --upgrade --force-reinstall numpy pandas streamlit --break-system-packages
```

### Summary of Changes:

- Enabled PDF parsing (`pypdf`).
- Added text chunking (`langchain-text-splitters`).
- Added vector database support (`chromadb`).
- Secured API key storage in Codespace environment.

## How to Use

1. Upload one or more `.txt` or `.pdf` files.
2. Wait for "Documents processed successfully!" to appear.
3. Type a question (e.g., "Summarize this document.").
4. The assistant retrieves relevant chunks and answers based on your files.
5. Continue chatting — conversation history is preserved.

## Troubleshooting

**If the Streamlit app does not open automatically:**

```bash
streamlit run chat_with_pdf.py
```

**If packages are missing:**

```bash
pip install -r requirements.txt
```

**To verify your API key:**

```bash
echo $OPENAI_API_KEY
```

## Reference Log (ref-log.md)

### External Tools and Libraries:

- **Streamlit** — web UI framework.
- **LangChain / LangChain-OpenAI / LangChain-Text-Splitters** — RAG pipeline components.
- **Chroma** — vector database for semantic search.
- **PyPDF** — PDF text extraction.
- **OpenAI API (Cornell proxy)** — embeddings and GPT-4o chat model.

### GenAI Usage:

- **Tool Used**: ChatGPT (GPT-5)
- **Purpose**: Helped format and debug Streamlit + LangChain code and draft documentation.
- **Rationale**: Used only for clarity and structure; final implementation and testing performed manually.

---