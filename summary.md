# 📄 Enterprise RBAC Chatbot - System Summary

## 🌟 Overview
The **Enterprise RBAC Chatbot** is a security-first AI assistant designed for corporate environments. It combines **Retrieval-Augmented Generation (RAG)** with a robust **Role-Based Access Control (RBAC)** layer, ensuring that employees can only access information authorized by their specific organizational role.

---

## 🏗️ The RAG Pipeline Architecture

The system follows a multi-stage pipeline to transform raw documents into secure, context-aware AI responses:

### 1. Data Ingestion & Preprocessing (Week 1 & 2)
- **Parsing**: Documents (Markdown, CSV) are parsed into raw text.
- **Chunking**: Text is split into smaller, meaningful "chunks" (approx. 500-1000 characters) using LangChain's recursive splitters. This ensures the LLM receives relevant context without exceeding token limits.
- **Metadata Tagging**: Each chunk is tagged with its source department (e.g., Finance, HR, Engineering). This is the foundation of the RBAC system.

### 2. Vectorization & Storage (Week 3)
- **Embeddings**: We use the `all-MiniLM-L6-v2` Sentence-Transformer model to convert text chunks into high-dimensional numerical vectors (embeddings).
- **Vector Database**: These vectors are stored in **ChromaDB**, a high-performance vector database that allows for semantic search rather than just keyword matching.

### 3. Secure Search & RBAC Filtering (Week 4)
- **Query Processing**: When a user asks a question, the query is also converted into a vector.
- **Semantic Retrieval**: The system finds the top most similar chunks in ChromaDB.
- **RBAC Filter**: Before passing data to the AI, a custom filtering layer checks the user's JWT (JSON Web Token) role against the document metadata.
    - *Example*: An `hr_user` can see `HR` and `General` documents, but `Finance` documents are strictly blocked and removed from the context.

### 4. Response Generation - RAG (Week 5 & 6)
- **Context Injection**: Only the authorized chunks are sent to the Large Language Model (LLM).
- **The Prompt**: The AI is instructed: *"Use ONLY the provided context. If the answer isn't there, say you don't know."*
- **LLM Provider**: The system is currently configured to use **Hugging Face Inference API** with the `microsoft/Phi-3-mini-4k-instruct` model. This provides a fast, efficient, and intelligent reasoning engine.

---

## 🔑 LLM & API Configuration

The system is flexible and can switch between Cloud and Local deployments:

| Provider | Model | Connection Type |
|---|---|---|
| **Hugging Face** (Current) | `microsoft/Phi-3-mini-4k-instruct` | Cloud API (Requires Key) |
| **Ollama** (Fallback) | `llama3.2:3b` | 100% Local (Privacy Focused) |

### Current Active Configuration (`.env`):
- **Base URL**: `https://router.huggingface.co/hf-inference/v1/`
- **Model**: `microsoft/Phi-3-mini-4k-instruct`
- **X-LLM-API-KEY**: Managed via the user's Hugging Face account tokens.

---

## 🔒 Security Summary
- **Authentication**: Secure login using FastAPI and JWT.
- **Authorization**: Granular access control at the document level.
- **Privacy**: No data leakage between departments.
- **Auditability**: All queries track which documents were retrieved and the similarity scores.

## 🏁 Conclusion
By bridging the gap between advanced AI capabilities and strict enterprise security requirements, this system provides a safe way to deploy LLMs in corporate environments, protecting proprietary data while empowering employees with instant information access.
