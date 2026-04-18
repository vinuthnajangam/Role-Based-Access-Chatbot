import os
import json
from sentence_transformers import SentenceTransformer

def generate_embeddings():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    input_file = os.path.join(base_dir, '..', '..', 'week 2', 'output', 'chunked_documents.json')
    output_file = os.path.join(base_dir, '..', 'output', 'chunk_embeddings.json')
    
    if not os.path.exists(input_file):
        print(f"Input file not found: {input_file}")
        return

    # Load chunks
    with open(input_file, 'r', encoding='utf-8') as f:
        chunks = json.load(f)
        
    print(f"Loading SentenceTransformer model 'all-MiniLM-L6-v2'...")
    model = SentenceTransformer('all-MiniLM-L6-v2')
    
    print(f"Generating embeddings for {len(chunks)} chunks...")
    
    embedded_data = []
    
    try:
        # Batch processing could be faster but let's keep it simple for now
        for i, chunk in enumerate(chunks):
            content = chunk.get("content", "")
            # Generate embedding
            embedding = model.encode(content)
            
            embedded_data.append({
                "chunk_id": chunk.get("chunk_id"),
                "content": content,
                "source_file": chunk.get("source_file"),
                "embedding": embedding.tolist() # Convert numpy array to list for JSON serialization
            })
            
            if (i+1) % 10 == 0:
                print(f"Generated embedding for chunk {i+1}/{len(chunks)}")
                
    except Exception as e:
        print(f"Error generating embeddings: {e}")
        
    # Save output
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(embedded_data, f, indent=2)
        
    print(f"Total embeddings: {len(embedded_data)}")
    print(f"Dimension: {len(embedded_data[0]['embedding'])}")
    print(f"Saved to {output_file}")

if __name__ == "__main__":
    generate_embeddings()
