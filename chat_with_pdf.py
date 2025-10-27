# ============================================================================
# RAG (Retrieval-Augmented Generation) Application with Streamlit
# ============================================================================
# This app allows users to upload documents (.txt, .md, .pdf) and ask questions
# about their content. It uses:
# 1. Document chunking (breaking large docs into smaller pieces)
# 2. Embeddings (converting text to numerical vectors)
# 3. Vector database (Chroma - for fast semantic search)
# 4. LLM (GPT-4o - for generating answers based on retrieved context)
# ============================================================================

import streamlit as st  # Web app framework
import os
from openai import OpenAI  # For calling GPT models
from typing import List
import io
from pypdf import PdfReader  # For reading PDF files

# LangChain imports - framework for building LLM applications
from langchain_core.documents import Document  # Document object with content + metadata
from langchain_text_splitters import RecursiveCharacterTextSplitter  # Smart text chunking
from langchain_openai import OpenAIEmbeddings  # Converts text to vector embeddings
from langchain.vectorstores import Chroma  # Vector database for storing and searching embeddings

# ============================================================================
# SETUP: Configure API access for both OpenAI client and LangChain
# ============================================================================

# Direct OpenAI client for chat completions (the actual chat interface)
client = OpenAI(
    api_key=os.environ["OPENAI_API_KEY"],
    base_url="https://api.ai.it.cornell.edu",
)

# ============================================================================
# STREAMLIT UI SETUP
# ============================================================================

st.title("📝 File Q&A with RAG")

# File uploader widget - allows multiple files of different types
uploaded_files = st.file_uploader(
    "Upload article(s)", 
    type=("txt", "md", "pdf"),  # Supported file types
    accept_multiple_files=True   # Allow uploading multiple documents at once
)

# ============================================================================
# SESSION STATE: Store data that persists across user interactions
# ============================================================================
# Streamlit reruns the entire script on every interaction, so we need to
# store important data in st.session_state to avoid losing it

# Chat history - stores all messages between user and assistant
if "messages" not in st.session_state:
    st.session_state["messages"] = [
        {"role": "assistant", "content": "Upload documents and ask me anything about them!"}
    ]

# Vector store - contains all embedded document chunks (this is our "knowledge base")
if "vectorstore" not in st.session_state:
    st.session_state["vectorstore"] = None

# Track which files we've already processed (to avoid reprocessing on every interaction)
if "processed_files" not in st.session_state:
    st.session_state["processed_files"] = set()  # Set of filenames


# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

def build_vectorstore_from_files(files: List) -> Chroma:
    """
    Build a vector store from uploaded files.
    
    This is the core RAG setup function. It:
    1. Reads all uploaded files
    2. Splits them into small chunks
    3. Converts chunks to vector embeddings
    4. Stores embeddings in a searchable database (Chroma)
    
    Args:
        files: List of Streamlit UploadedFile objects
        
    Returns:
        Chroma: Vector database containing all document chunks
    """
    docs: List[Document] = []
    
    # Step 1: Read each file and create Document objects
    for file in files:
        text = read_file_to_text(file)
        
        # Skip empty files
        if not text.strip():
            st.warning(f"Skipping empty file: {file.name}")
            continue
            
        # Create LangChain Document with content + metadata
        # Metadata tracks which file this text came from
        docs.append(Document(
            page_content=text,
            metadata={"source": file.name}
        ))
    
    # Validation: make sure we have at least one valid document
    if not docs:
        st.error("No valid documents to process!")
        return None
    
    # Step 2: Split documents into smaller chunks
    # Why? Large documents don't fit in LLM context windows, and smaller
    # chunks give more precise retrieval
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=200,      # Each chunk ~200 characters
        chunk_overlap=0      # No overlap between chunks (can adjust for context)
    )
    chunks = text_splitter.split_documents(docs)
    
    st.info(f"Created {len(chunks)} chunks from {len(docs)} document(s)")
    
    # Step 3: Create embeddings and vector store
    # Embeddings convert text to numbers (vectors) that capture meaning
    # Similar text = similar vectors, enabling semantic search
    
    # IMPORTANT: Must use "openai." prefix when using Cornell proxy
    embeddings = OpenAIEmbeddings(model="openai.text-embedding-3-large")
    
    # Create Chroma vector database from chunks
    # This computes embeddings for all chunks and stores them for fast search
    vectorstore = Chroma.from_documents(documents=chunks, embedding=embeddings)
    
    return vectorstore


def retrieve_context(vectorstore: Chroma, query: str, k: int = 20) -> List[Document]:
    """
    Retrieve the most relevant document chunks for a query.
    
    This performs "semantic search" - finding chunks whose meaning is similar
    to the query, even if the exact words don't match.
    
    Args:
        vectorstore: The Chroma database to search
        query: User's question
        k: Number of chunks to retrieve (default 20)
        
    Returns:
        List[Document]: Top-k most relevant chunks
    """
    # Create a retriever object configured for similarity search
    retriever = vectorstore.as_retriever(
        search_type="similarity",  # Use semantic similarity (vs. keyword matching)
        search_kwargs={"k": k}     # Return top-k results
    )
    
    # Perform the search and return relevant documents from similarity search
    return vectorstore.similarity_search(query, k=k)

def format_context(docs: List[Document]) -> str:
    """
    Format retrieved documents into a readable context string.
    
    Adds source attribution so we know which file each chunk came from.
    This is important for citation and debugging.
    
    Args:
        docs: List of retrieved Document objects
        
    Returns:
        str: Formatted context with source labels
    """
    parts = []
    for i, doc in enumerate(docs, 1):
        # Get source filename from metadata
        source = doc.metadata.get("source", "unknown")
        # Format with numbering and source info
        parts.append(f"[Chunk {i} from {source}]:\n{doc.page_content.strip()}")
    
    # Join all chunks with blank lines between them
    return "\n\n".join(parts)


# ============================================================================
# DOCUMENT PROCESSING
# ============================================================================
# This section handles building/rebuilding the vector store when files change

if uploaded_files:
    # Get current set of filenames
    current_files = set(f.name for f in uploaded_files)
    
    # Check if files have changed since last processing
    # Only rebuild if files are different (saves time and API calls)
    if current_files != st.session_state["processed_files"]:
        with st.spinner("Processing documents..."):
            # Build the vector store (this calls the embedding API)
            st.session_state["vectorstore"] = build_vectorstore_from_files(uploaded_files)
            # Update our record of which files we've processed
            st.session_state["processed_files"] = current_files
        st.success("Documents processed successfully!")

# ============================================================================
# CHAT INTERFACE
# ============================================================================

# Display all previous messages in the chat history
for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

# Chat input box - disabled until documents are uploaded and processed
question = st.chat_input(
    "Ask something about the article(s)",
    disabled=not uploaded_files or st.session_state["vectorstore"] is None
)

# ============================================================================
# RAG QUERY PROCESSING
# ============================================================================
# This is where the RAG magic happens! When user asks a question:
# 1. Retrieve relevant chunks from vector store
# 2. Build a context-aware prompt
# 3. Generate an answer using the LLM

if question and st.session_state["vectorstore"]:
    # Step 1: Add user's question to chat history
    st.session_state.messages.append({"role": "user", "content": question})
    st.chat_message("user").write(question)
    
    # Step 2: RETRIEVAL - Find relevant chunks from our documents
    with st.spinner("Searching documents..."):
        # Use semantic search to find top-k relevant chunks
        top_docs = retrieve_context(st.session_state["vectorstore"], question, k=20)
        # Format chunks into readable context string
        context_text = format_context(top_docs)
    
    # Step 3: AUGMENTATION - Build system prompt with retrieved context
    # This is the key to RAG: we give the LLM relevant context before asking the question
    system_prompt = (
        "You are a helpful assistant for question-answering tasks.\n"
        "Use ONLY the following context to answer the question.\n"  # Force grounding
        "If you don't know the answer from the context, say you don't know.\n"  # Prevent hallucination
        "Keep your answer concise (3 sentences maximum).\n\n"
        f"Context:\n{context_text}"  # Insert retrieved chunks here
    )
    
    # Step 4: GENERATION - Call the LLM to generate an answer
    with st.chat_message("assistant"):
        # Stream the response for better UX (shows text as it's generated)
        stream = client.chat.completions.create(
            model="openai.gpt-4o",  # Use GPT-3.5 Turbo model
            messages=[
                {"role": "system", "content": system_prompt},  # System prompt with context
                {"role": "user", "content": question}          # User's question
            ],
            stream=True  # Enable streaming for real-time display
        )
        # Display streaming response in Streamlit
        response = st.write_stream(stream)
    
    # Step 5: Save assistant's response to chat history
    st.session_state.messages.append({"role": "assistant", "content": response})