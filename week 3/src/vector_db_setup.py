import os
import json
import chromadb
from chromadb.config import Settings

def get_db_path():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(base_dir, '..', 'output', 'vector_db')

def setup_vector_db():
    persist_dir = get_db_path()
    
    # Initialize Chroma Client
    client = chromadb.PersistentClient(path=persist_dir)
    
    collection_name = "rbac_documents"
    
    # Get or create collection
    # distance function defaulting to cosine (or l2 in some versions, but we can specify)
    # metadata={"hnsw:space": "cosine"}
    collection = client.get_or_create_collection(
        name=collection_name,
        metadata={"hnsw:space": "cosine"}
    )
    
    print(f"Vector database initialized at: {persist_dir}")
    print(f"Collection '{collection_name}' ready.")
    
    return collection

def get_collection():
    persist_dir = get_db_path()
    client = chromadb.PersistentClient(path=persist_dir)
    return client.get_collection(name="rbac_documents")

if __name__ == "__main__":
    setup_vector_db()
