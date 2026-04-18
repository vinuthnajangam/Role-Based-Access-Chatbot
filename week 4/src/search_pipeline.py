import sys
import os
import json
import logging

# Paths
base_dir = os.path.dirname(os.path.abspath(__file__))
week3_src = os.path.join(base_dir, '..', '..', 'week 3', 'src')
sys.path.append(week3_src)

# Imports
try:
    from semantic_search import SemanticSearch
except ImportError:
    print("Error importing SemanticSearch. Make sure week 3/src is correct.")
    
from query_processor import QueryProcessor
from rbac_filter import RBACFilter
from chunk_selector import ChunkSelector

# Logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class SearchPipeline:
    def __init__(self):
        logger.info("Initializing Search Pipeline...")
        self.processor = QueryProcessor()
        self.searcher = SemanticSearch()
        self.rbac = RBACFilter()
        self.selector = ChunkSelector()
        
    def search(self, query, user_role, top_k=5):
        logger.info(f"Pipeline Start: q='{query}' role='{user_role}'")
        
        # 1. Preprocess Query
        processed_query = self.processor.preprocess(query)
        logger.info(f"Processed Query: {processed_query}")
        
        # 2. Vector Search (Get more results than needed to allow for filtering)
        # Fetching 5x top_k to ensure we have enough after RBAC
        raw_results = self.searcher.search(processed_query, n_results=top_k * 5)
        logger.info(f"Vector Search Found: {len(raw_results)}")
        
        # 3. RBAC Filtering
        filtered_results = self.rbac.filter_by_role(user_role, raw_results)
        logger.info(f"After RBAC Filter: {len(filtered_results)}")
        
        # 4. Chunk Selection (Re-ranking/Thresholding)
        final_results = self.selector.select_chunks(filtered_results)
        # Limit to top_k again just in case selector logic differs
        final_results = final_results[:top_k]
        logger.info(f"Final Selection: {len(final_results)}")
        
        return {
            "query": query,
            "processed_query": processed_query,
            "results": final_results,
            "total_found": len(raw_results),
            "filtered_count": len(raw_results) - len(filtered_results)
        }

if __name__ == "__main__":
    pipeline = SearchPipeline()
    
    # Test Scenario
    q = "Q4 revenue"
    role = "finance"
    
    res = pipeline.search(q, role)
    
    print("\nSearch Results:")
    for r in res['results']:
        print(f"[{r['metadata'].get('department')}] {r['content'][:50]}... (Score: {r['score']:.4f})")
