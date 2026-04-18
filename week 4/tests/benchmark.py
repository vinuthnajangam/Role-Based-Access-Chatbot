import sys
import os
import json
import time

base_dir = os.path.dirname(os.path.abspath(__file__))
src_path = os.path.join(base_dir, '..', 'src')
sys.path.append(src_path)

from search_pipeline import SearchPipeline

def run_benchmark():
    pipeline = SearchPipeline()
    
    query_file = os.path.join(base_dir, 'benchmark_queries.json')
    if not os.path.exists(query_file):
        print("Queries file missing.")
        return
        
    with open(query_file, 'r') as f:
        data = json.load(f)
        queries = data['queries']
        
    print(f"\nRunning Benchmark on {len(queries)} queries...")
    print("-" * 80)
    print(f"| {'Query':<20} | {'Role':<10} | {'Expected':<10} | {'Result':<10} | {'Time(ms)':<8} |")
    print("-" * 80)
    
    total_time = 0
    passed = 0
    results_list = []
    
    for item in queries:
        start = time.time()
        res = pipeline.search(item['query'], item['role'])
        latency = (time.time() - start) * 1000
        
        top_res = res['results'][0] if res['results'] else None
        actual_dept = top_res['metadata']['department'] if top_res else "None"
        
        # Check success
        # Note: RBAC might block correct dept if logic assumes user shouldn't see it?
        # But here 'expected_dept' implies what logic SHOULD return.
        
        is_match = actual_dept.lower() == item['expected_dept'].lower()
        if is_match: passed += 1
        
        print(f"| {item['query'][:20]:<20} | {item['role']:<10} | {item['expected_dept']:<10} | {actual_dept:<10} | {latency:.2f}     |")
        
        results_list.append({
            "query": item['query'],
            "role": item['role'],
            "latency": latency,
            "success": is_match
        })
        
        total_time += latency
        
    print("-" * 80)
    print(f"Accuracy: {passed}/{len(queries)} ({(passed/len(queries))*100:.1f}%)")
    print(f"Avg Latency: {total_time/len(queries):.2f} ms")
    
    # Save output
    outfile = os.path.join(base_dir, '..', 'output', 'benchmark_results.json')
    with open(outfile, 'w') as f:
        json.dump(results_list, f, indent=2)

if __name__ == "__main__":
    run_benchmark()
