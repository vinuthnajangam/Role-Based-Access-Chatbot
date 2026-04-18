import os
import chromadb
from sentence_transformers import SentenceTransformer
# We can reuse setup from index/vector_db but let's keep it self-contained or import
from vector_db_setup import get_collection

class SemanticSearch:
    def __init__(self):
        print("Initializing Semantic Search...")
        self.model = SentenceTransformer('all-MiniLM-L6-v2')
        self.collection = get_collection()
        
    def search(self, query, n_results=5):
        query_embedding = self.model.encode(query).tolist()
        
        results = self.collection.query(
            query_embeddings=[query_embedding],
            n_results=n_results
        )
        
        # Parse results into a cleaner format
        parsed_results = []
        if results['ids']:
            count = len(results['ids'][0])
            for i in range(count):
                parsed_results.append({
                    "chunk_id": results['ids'][0][i],
                    "content": results['documents'][0][i],
                    "metadata": results['metadatas'][0][i],
                    "score": results['distances'][0][i] if 'distances' in results else 0
                })
        
        return parsed_results

    def search_with_filter(self, query, department, n_results=5):
        query_embedding = self.model.encode(query).tolist()
        
        results = self.collection.query(
            query_embeddings=[query_embedding],
            n_results=n_results,
            where={"department": department}
        )
        
        parsed_results = []
        if results['ids']:
            count = len(results['ids'][0])
            for i in range(count):
                parsed_results.append({
                    "chunk_id": results['ids'][0][i],
                    "content": results['documents'][0][i],
                    "metadata": results['metadatas'][0][i],
                    "score": results['distances'][0][i]
                })
        return parsed_results

def test_search():
    searcher = SemanticSearch()
    
    test_queries = [
        "What is the Q4 revenue?",
        "Employee leave policy",
        "Marketing campaign results"
    ]
    
    for q in test_queries:
        print(f"\nQuery: {q}")
        results = searcher.search(q, n_results=3)
        for r in results:
            dept = r['metadata'].get('department')
            print(f"- [{dept}] {r['content'][:50]}... (Score: {r['score']:.4f})")

if __name__ == "__main__":
    test_search()
