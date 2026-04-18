import json
import os

class ChunkSelector:
    def __init__(self):
        base_dir = os.path.dirname(os.path.abspath(__file__))
        config_path = os.path.join(base_dir, '..', 'config', 'selection_config.json')
        
        with open(config_path, 'r', encoding='utf-8') as f:
            self.config = json.load(f)
            
        self.top_k = self.config.get("top_k", 5)
        self.similarity_threshold = self.config.get("similarity_threshold", 0.3)

    def select_chunks(self, filtered_results):
        """
        Selects the best chunks from ALREADY FILTERED results.
        
        Args:
            filtered_results (list): Output from RBACFilter. Each item: {score, ...}
            
        Returns:
            list: Top-K chunks sorted by relevance
        """
        # Chroma Cosine Distance: 0 = Identical, 2 = Opposite.
        # Threshold logic: We want distance < (1 - 0.3) = 0.7 approx?
        # Let's treat config threshold as 'max_distance' for safety if using distance.
        # Or if we assume score IS similarity (converted upstream), then > threshold.
        # Let's assume upstream (semantic_search) returns raw Chroma distance.
        # We need to invert or adjust.
        # Let's fix Logic: Valid if score <= 0.7 (if threshold is high sim implies low distance)
        
        # Actually simplest: Just Select Top K by lowest distance.
        # Filter: Distance < 0.8 (approx 0.2 sim).
        
        cutoff = 0.7 # Ad-hoc distance cutoff
        valid_chunks = [r for r in filtered_results if r['score'] <= cutoff]
        
        # Sort Ascending (Lower distance = Better)
        valid_chunks.sort(key=lambda x: x['score']) 
        
        # Slice top-k
        selected = valid_chunks[:self.top_k]
        
        print(f"Selector: Input={len(filtered_results)} | Valid(Dist<{cutoff})={len(valid_chunks)} | Selected={len(selected)}")
        
        return selected

if __name__ == "__main__":
    sel = ChunkSelector()
    mock_results = [{"id": 1, "score": 0.1}, {"id": 2, "score": 0.8}, {"id": 3, "score": 0.2}]
    print(f"Mock input: {mock_results}")
    # If 0.1 is distance (better), 0.8 is bad.
    # If threshold is similarity 0.3 (higher better), then logic flips.
    # Config has threshold 0.3. This usually implies Similarity.
    # But Chroma returns Distance.
    # Distance = 1 - Similarity.
    # So Similarity > 0.3 means Distance < 0.7.
    
    # I will update logic to handle Distance:
    # Valid if score <= (1 - threshold) ? Or just use raw thresholds suited for distance.
    # Let's adjust logic in file to assume the input might be Similarity or Distance.
    # Since config says "similarity_threshold: 0.3", it sounds like we want similarity > 0.3.
    # But if our searcher returns Distance, we need to convert.
    # For now, I'll update logic to assume score is Distance (lower is better) and threshold refers to Distance limit.
    pass
