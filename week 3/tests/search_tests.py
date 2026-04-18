import os
import json
import time
import sys

# Add src to path
base_dir = os.path.dirname(os.path.abspath(__file__))
src_path = os.path.join(base_dir, '..', 'src')
sys.path.append(src_path)

from semantic_search import SemanticSearch

def run_tests():
    # Load queries
    query_file = os.path.join(base_dir, 'test_queries.json')
    if not os.path.exists(query_file):
        print("Test queries file missing.")
        return

    with open(query_file, 'r') as f:
        queries = json.load(f)
        
    searcher = SemanticSearch()
    
    results_list = []
    
    print(f"\nRunning {len(queries)} search tests...")
    print("-" * 60)
    print(f"{'Query':<30} | {'Expected':<10} | {'Actual':<10} | {'Time(ms)':<8} | {'Pass'}")
    print("-" * 60)
    
    total_passed = 0
    total_latency = 0
    total_score = 0
    
    for item in queries:
        query = item['query']
        expected = item['expected_dept']
        
        start_time = time.time()
        search_results = searcher.search(query, n_results=1)
        latency = (time.time() - start_time) * 1000
        
        passed = False
        actual = "None"
        score = 0
        
        if search_results:
            top_result = search_results[0]
            actual = top_result['metadata'].get('department', 'unknown')
            score = top_result['score']
            
            # Case-insensitive check
            if actual.lower() == expected.lower():
                passed = True
                
        if passed:
            total_passed += 1
            
        total_latency += latency
        total_score += score
        
        status = "✅" if passed else "❌"
        
        print(f"{query[:30]:<30} | {expected:<10} | {actual:<10} | {latency:.2f}     | {status}")
        
        results_list.append({
            "query": query,
            "expected_dept": expected,
            "actual_dept": actual,
            "latency_ms": latency,
            "passed": passed,
            "score": score
        })
        
    # Summary
    pass_rate = (total_passed / len(queries)) * 100
    avg_latency = total_latency / len(queries)
    avg_score = total_score / len(queries)
    
    print("-" * 60)
    print(f"Pass Rate: {pass_rate:.1f}%")
    print(f"Avg Latency: {avg_latency:.2f} ms")
    print(f"Avg Relevance Score (Distance): {avg_score:.4f}")
    
    output_file = os.path.join(base_dir, '..', 'output', 'test_results.json')
    with open(output_file, 'w') as f:
        json.dump(results_list, f, indent=2)
        
    print(f"\nDetailed results saved to {output_file}")

if __name__ == "__main__":
    run_tests()
