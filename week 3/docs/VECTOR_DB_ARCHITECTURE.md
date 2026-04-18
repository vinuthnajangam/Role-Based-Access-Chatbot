# Vector Database Architecture
**Author:** Sri Saranya Chandrapati

## 1. Overview
The vector database is the core retrieval engine for the RBAC Chatbot. It stores high-dimensional vector representations of document chunks to enable semantic search. We utilize **ChromaDB** for its lightweight, local persistence and ease of integration.

## 2. Embedding Model
- **Model:** `sentence-transformers/all-MiniLM-L6-v2`
- **Dimension:** 384
- **Reasoning:** 
  - Fast inference (optimized for CPU/low-resource)
  - Good semantic grasp for technical/business domains
  - Small storage footprint

## 3. Architecture Flow
```ascii
DOCUMENT 
   ⬇️
[CHUNKING] (512 tokens)
   ⬇️
[EMBEDDING] (Transformer Model) -> [Vector 384d]
   ⬇️
[INDEXING] -> ChromaDB Collection "rbac_documents"
   Checking: IDs, Embeddings, Metadata
   ⬇️
[QUERY] -> Vector Search -> Top-K Results
```

## 4. Collection Schema
The ChromaDB collection `rbac_documents` stores:

| Field | Type | Description |
|---|---|---|
| `id` | String | Unique Chunk ID (e.g., `chunk_0042`) |
| `embedding` | List[Float] | 384-dimensional vector |
| `document` | String | Original text content of the chunk |
| `metadata` | Dict | `{ "department": "Finance", "accessible_roles": "finance,c-level", "source": "report.md" }` |

## 5. Query Logic
1.  **Input:** User text query.
2.  **Embed:** Convert query to vector using the same model.
3.  **Search:** Perform Cosine Similarity matching in ChromaDB.
4.  **Filter (Optional):** Apply `where={"department": "..."}` for strict filtering (used in RBAC later).
5.  **Output:** List of relevant chunks with similarity scores.

## 6. Performance
Current benchmarks show <40ms latency for search, which exceeds the <500ms requirement.
