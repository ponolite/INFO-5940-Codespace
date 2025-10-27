# INFO 5940 — Retrieval-Augmented Generation (RAG) Application

Welcome to the **INFO 5940 Assignment 1** repository. This assignment project constructs a **Retrieval-Augmented Generation (RAG)** system using **Streamlit**, **LangChain**, **Chroma**, and **OpenAI**.  

The RAG enables users to upload `.txt`, `.md` and `.pdf` files and discuss their content through a conversational chat interface.

## Getting Started

### Step 1 – Initiate Your Forked Repository
1. Fork the class repository to your GitHub account.
2. Use the green **Code** button to open the **Codespaces** tab and choose **Create Codespace**.
3. Wait for the environment to finish building (Python 3.11.13).

### Step 2 – Verify Your Environment
1. The **Python 3.11** kernel is already encoded within `.devcontainer`.
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

When prompted, choose **Open in Browser** to view the app interface in an external tab.

## Application Overview

### What the Application Does

1. Enables you to upload one or more `.txt` and `.pdf` files.
2. Extract and chunk text automatically for efficient retrieval.
3. Generate vector embeddings with OpenAI's `text-embedding-3-large` model.
4. Store and retrieve document chunks from a Chroma vector database.
5. Ask questions through a chat interface powered by streamlit.
6. Receive concise, contextualzed answers drawn directly from the uploaded materials.

### Application Features

- **Multi-file Upload**: supports `.txt`, `.pdf`, and `.md` documents.
- **Automatic PDF Parsing**: extracts text from PDF pages using PyPDF.
- **Document Chunking**: splits text into ~200-character chunks (no overlap).
- **Vector Embeddings**: uses OpenAI `text-embedding-3-large` model.
- **Semantic Retrieval**: performs similarity search with Chroma (k = 20).
- **Conversational Chat**: GPT-4o provides concise, context-based answers.
- **Multi-Turn Memory**: chat history stored in `st.session_state`.
- **Live Responses**: messages appear in real time in the UI.

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
```

- **`chromadb>=0.5.5`** – installs Chroma (v 0.5.5 or higher) for vector storage and retrieval.
- **`langchain-text-splitters`** – enables the application to split large documents into smaller chunks for RAG.

**Added Python import in main script:**

```python
from pypdf import PdfReader  # PDF reader
```

**Encoded API Key securely inside Codespace:**

```
${localEnv:OPENAI_API_KEY}
```

Stores the OpenAI API key as a secret variable (and call it within `.devcontainer`) so it is not exposed in source control.

**Optional reinstall command used to fix dependency conflicts:**

```bash
pip install --upgrade --force-reinstall numpy pandas streamlit --break-system-packages
```

### Summary of Changes:

- Allowed for PDF parsing (`pypdf`).
- Enabled text chunking (`langchain-text-splitters`).
- Enabled vector database support (`chromadb`).
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
- **LangChain / LangChain-OpenAI / LangChain-Text-Splitters** — RAG structure & components.
- **Chroma** — vector database for semantic search.
- **PyPDF** — PDF text extraction.
- **OpenAI API (Cornell proxy)** — embeddings and GPT-4o chat model.

### GenAI Usage:

- **Tool Used**: ChatGPT (GPT-5)
- **Purpose**: Helped format and debug Streamlit + create helper functions + LangChain code and draft documentation.
- **Rationale**: Used only for code organization, clarity as well as structure; final implementation and testing performed manually. See `ref-log.md` for more details.