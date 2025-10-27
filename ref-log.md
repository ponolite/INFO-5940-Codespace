# Reference Log

This document tracks all external sources, tools, libraries, and GenAI usage for the INFO 5940 RAG Application assignment.


## External Tools and Libraries

### Core Frameworks and Libraries

#### Streamlit
- **Purpose**: Web application framework for building the interactive chat interface
- **Documentation**: https://docs.streamlit.io/
- **Version Used**: Latest stable version
- **Usage**: Built the entire user interface including file upload, chat display, and session state management

#### LangChain
- **Purpose**: Framework for building LLM-powered applications
- **Documentation**: https://python.langchain.com/docs/
- **Components Used**:
  - `langchain-openai`: OpenAI integration for embeddings and chat models
  - `langchain-text-splitters`: Document chunking utilities
  - `langchain-chroma`: Chroma vector store integration
- **Usage**: Core RAG pipeline construction, document processing, and retrieval

#### Chroma
- **Purpose**: Vector database for storing and retrieving document embeddings
- **Documentation**: https://docs.trychroma.com/
- **Version**: >=0.5.5
- **Usage**: Semantic search and similarity-based document retrieval

#### PyPDF
- **Purpose**: PDF text extraction library
- **Documentation**: https://pypdf.readthedocs.io/
- **Usage**: Parsing and extracting text content from uploaded PDF files

#### OpenAI API
- **Purpose**: Language model and embedding services
- **Endpoint**: Cornell AI API proxy (https://api.ai.it.cornell.edu)
- **Models Used**:
  - `text-embedding-3-large`: Document embedding generation
  - `gpt-4o`: Conversational responses and question answering
- **Usage**: Generated embeddings for documents and provided intelligent responses to user queries


## Documentation and Learning Resources

### Official Documentation
- **Streamlit Documentation**: https://docs.streamlit.io/
  - Referenced for file uploader, session state, and chat interface components
  
- **LangChain Documentation**: https://python.langchain.com/docs/
  - Referenced for RAG implementation patterns and document processing
  
- **Chroma Documentation**: https://docs.trychroma.com/
  - Referenced for vector store setup and retrieval configuration

### GitHub Resources
- **GitHub Codespaces Documentation**: https://docs.github.com/en/codespaces
  - Referenced for understanding development environment setup
  - Used to configure `.devcontainer.json` for automatic dependency installation


## GenAI Usage Log

### ChatGPT (GPT-4/GPT-5)

#### Session 1: Initial Code Structure
- **Date**: [Insert date]
- **Purpose**: Generated boilerplate code for Streamlit app with file upload functionality
- **Rationale**: Accelerated initial setup and ensured best practices for Streamlit session state management
- **Specific Usage**:
  - Created basic Streamlit app structure
  - Implemented file uploader with multiple file type support
  - Set up session state for chat history
- **What Was Modified**: Adapted the generated code to work with Cornell's OpenAI API proxy and adjusted chunking parameters

#### Session 2: RAG Pipeline Implementation
- **Date**: [Insert date]
- **Purpose**: Debugged LangChain integration with Chroma vector store
- **Rationale**: Resolved dependency conflicts and API compatibility issues between LangChain versions
- **Specific Usage**:
  - Helped troubleshoot import errors with `langchain-chroma`
  - Suggested proper initialization of OpenAI embeddings with custom base URL
  - Provided example code for document chunking with `CharacterTextSplitter`
- **What Was Modified**: Adjusted retrieval parameters (k=20) and added error handling for empty documents

#### Session 3: PDF Processing
- **Date**: [Insert date]
- **Purpose**: Implemented PDF text extraction using PyPDF
- **Rationale**: Needed efficient way to handle multi-page PDF uploads
- **Specific Usage**:
  - Generated code for iterating through PDF pages
  - Provided text extraction logic using `PdfReader`
- **What Was Modified**: Added file type validation and combined text extraction with existing .txt file handling

#### Session 4: Documentation
- **Date**: [Insert date]
- **Purpose**: Formatted and structured README.md and ref-log.md
- **Rationale**: Ensured documentation matched INFO 5940 assignment style and formatting requirements
- **Specific Usage**:
  - Helped organize README sections with clear numbered steps
  - Drafted troubleshooting section
  - Formatted code blocks and configuration examples
- **What Was Modified**: Customized content to reflect actual implementation details and added Cornell-specific information


## Development Tools

### GitHub Codespaces
- **Purpose**: Cloud-based development environment
- **Configuration**: Pre-configured with Python 3.11.13 via `.devcontainer.json`
- **Usage**: Primary development and testing environment

### VS Code
- **Purpose**: Code editor (via Codespaces)
- **Extensions Used**: Python, Pylance (automatically installed)



## Testing and Verification

### Manual Testing
- Uploaded various `.txt` and `.pdf` files to verify document processing
- Tested multi-turn conversations to ensure chat history persistence
- Verified retrieval accuracy by asking specific questions about uploaded content
- Tested error handling with empty files and unsupported formats

### API Testing
- Verified OpenAI API connectivity through Cornell proxy
- Tested embedding generation with sample documents
- Confirmed GPT-4o response streaming functionality



## Notes

- All external libraries were installed via `pip` using `requirements.txt`
- OpenAI API key stored securely as environment variable (not committed to repository)
- No copyrighted or proprietary code was used beyond standard open-source libraries
- All GenAI-generated code was reviewed, tested, and modified to fit project requirements

---

**Last Updated**: [10/27/2025]