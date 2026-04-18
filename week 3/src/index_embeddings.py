import os
import json
import vector_db_setup
# But actually better to just import the function if in same dir
from vector_db_setup import setup_vector_db

def index_data():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    embeddings_file = os.path.join(base_dir, '..', 'output', 'chunk_embeddings.json')
    metadata_file = os.path.join(base_dir, '..', '..', 'week 2', 'output', 'tagged_chunks.json')
    
    if not os.path.exists(embeddings_file) or not os.path.exists(metadata_file):
        print("Input files missing.")
        return

    # Load data
    with open(embeddings_file, 'r', encoding='utf-8') as f:
        embeddings_data = json.load(f)
        
    with open(metadata_file, 'r', encoding='utf-8') as f:
        metadata_list = json.load(f)
        
    # Map metadata by chunk_id for easy lookup
    metadata_map = {item['chunk_id']: item for item in metadata_list}
    
    collection = setup_vector_db()
    
    # Prepare batch data
    ids = []
    embeddings = []
    documents = []
    metadatas = []
    
    batch_size = 100
    
    print(f"Indexing {len(embeddings_data)} documents...")
    
    for i, item in enumerate(embeddings_data):
        chunk_id = item['chunk_id']
        chunk_meta = metadata_map.get(chunk_id, {})
        
        ids.append(chunk_id)
        embeddings.append(item['embedding'])
        documents.append(item['content'])
        
        # Prepare metadata dict for Chroma
        # Chroma metadata values must be int, float, str, or bool. 
        # Lists (accessible_roles) need to be converted to string representation or handled differently.
        # We will join the list into a comma-separated string for storage.
        roles_str = ",".join(chunk_meta.get('accessible_roles', []))
        
        metadatas.append({
            "department": chunk_meta.get('department', 'unknown'),
            "accessible_roles": roles_str,
            "source": chunk_meta.get('source', 'unknown')
        })
        
        # Batch add
        if len(ids) >= batch_size:
            collection.add(
                ids=ids,
                embeddings=embeddings,
                documents=documents,
                metadatas=metadatas
            )
            print(f"Indexed batch {i+1}")
            ids = []
            embeddings = []
            documents = []
            metadatas = []

    # Final batch
    if ids:
        collection.add(
            ids=ids,
            embeddings=embeddings,
            documents=documents,
            metadatas=metadatas
        )
        print(f"Indexed final batch of {len(ids)}")
        
    print(f"Total indexed: {len(embeddings_data)} documents")

if __name__ == "__main__":
    index_data()
