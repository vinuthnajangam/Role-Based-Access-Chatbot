import os
import time
import json
import sys
import numpy as np
from sentence_transformers import SentenceTransformer

# Add src to path
base_dir = os.path.dirname(os.path.abspath(__file__))
src_path = os.path.join(base_dir, '..', 'src')
sys.path.append(src_path)

from semantic_search import SemanticSearch

def run_benchmark():
    print("Starting Performance Benchmark...")
    results = {}
    
    # 1. Embedding Benchmark
    print("Benchmarking Embedding Generation...")
    model = SentenceTransformer('all-MiniLM-L6-v2')
    sample_text = "This is a sample document content for benchmarking purposes." * 10
    
    # Single doc
    start = time.time()
    model.encode(sample_text)
    single_time = (time.time() - start) * 1000
    
    # Batch 10
    start = time.time()
    model.encode([sample_text] * 10)
    batch_time = (time.time() - start) * 1000
    
    results['embedding'] = {
        "single_doc_ms": single_time,
        "batch_10_doc_ms": batch_time,
        "avg_per_doc_ms": batch_time / 10
    }
    
    # 2. Search Benchmark
    print("Benchmarking Search latency...")
    searcher = SemanticSearch()
    queries = ["revenue", "policy", "code", "marketing", "hiring"] * 2 # 10 queries
    
    latencies = []
    for q in queries:
        start = time.time()
        searcher.search(q)
        latencies.append((time.time() - start) * 1000)
    
    results['search'] = {
        "avg_latency_ms": np.mean(latencies),
        "p95_latency_ms": np.percentile(latencies, 95),
        "min_latency_ms": np.min(latencies),
        "max_latency_ms": np.max(latencies)
    }
    
    # Output results
    output_file = os.path.join(base_dir, '..', 'output', 'benchmark_results.json')
    with open(output_file, 'w') as f:
        json.dump(results, f, indent=2)
        
    print("\nBenchmark Results:")
    print("-" * 40)
    print(f"Embedding (1 doc):       {single_time:.2f} ms")
    print(f"Embedding (Avg batch):   {batch_time/10:.2f} ms")
    print("-" * 40)
    print(f"Search Avg Latency:      {np.mean(latencies):.2f} ms")
    print(f"Search P95 Latency:      {np.percentile(latencies, 95):.2f} ms")
    print("-" * 40)
    print(f"Saved to {output_file}")

if __name__ == "__main__":
    run_benchmark()
