# Reference Log

This `.md` file documents all external sources, tools, libraries, and GenAI usage for the INFO 5940 RAG Application Assignment 1.

## External Tools and Libraries

### Core Frameworks and Libraries

#### Streamlit
- **Purpose**: Web application structural framework to build the interactive conversational AI interface
- **Documentation**: https://docs.streamlit.io/
- **Usage**: Enable the building of the UI, including file file upload, chat display, and session state operation.

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
- **Date**: 10/25/2025
- **Purpose**: Generated re-usable, setup code for Streamlit app with file upload functionality
- **Rationale**: Accelerated initial setup and ensured best practices for Streamlit session state management
- **Specific Usage**:
  - Created basic Streamlit app structure
  - Implemented file uploader with multiple file type support
  - Set up session state for chat history
- **What Was Modified**: Adapted the generated code to work with Cornell's OpenAI API proxy and adjusted chunking parameters

#### Session 2: RAG Pipeline Implementation
- **Date**: 10/25/2025
- **Purpose**: Debugged LangChain integration with Chroma vector store
- **Rationale**: Resolved dependency conflicts and API compatibility issues between LangChain versions
- **Specific Usage**:
  - Helped troubleshoot import errors with `langchain-chroma`
  - Suggested proper initialization of OpenAI embeddings with custom base URL
  - Provided example code for document chunking with `CharacterTextSplitter`
- **What Was Modified**: Adjusted retrieval parameters (k=20) and added error handling for empty documents

#### Session 3: PDF Processing
- **Date**: 10/26/2025
- **Purpose**: Implemented PDF text extraction using PyPDF
- **Rationale**: Needed efficient way to handle multi-page PDF uploads
- **Specific Usage**:
  - Generated code for iterating through PDF pages
  - Provided text extraction logic using `PdfReader`
- **What Was Modified**: Added file type validation and combined text extraction with existing .txt file handling

#### Session 4: Documentation
- **Date**: 10/26/2025
- **Purpose**: Formatted and structured README.md and ref-log.md
- **Rationale**: Ensured documentation matched INFO 5940 assignment style and formatting requirements
- **Specific Usage**:
  - Helped organize README sections with clear numbered steps
  - Drafted troubleshooting section
  - Formatted code blocks and configuration examples
- **What Was Modified**: Customized content to reflect actual implementation details and added Cornell-specific information

## Testing and Verification

### Manual Testing
- Dropped and uploaded various `.txt` and `.pdf` files to ensure successful document processing
- Tested multi-turn conversations to ensure chatability
- Ensured retrieval accuracy by posing specific questions about uploaded content

## Notes

- All external libraries were installed via `pip` using `requirements.txt`
- OpenAI API key stored securely as environment variable (not committed to repository)
- All GenAI-generated code was reviewed, tested, and modified to fit project requirements

**Last Updated**: [10/27/2025]