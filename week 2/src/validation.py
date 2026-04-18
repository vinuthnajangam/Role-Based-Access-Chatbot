import os
import json
import tiktoken

def run_validation():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    input_file = os.path.join(base_dir, '..', 'output', 'tagged_chunks.json')
    output_file = os.path.join(base_dir, '..', 'output', 'validation_results.json')
    
    if not os.path.exists(input_file):
        print("tagged_chunks.json not found.")
        return

    with open(input_file, 'r', encoding='utf-8') as f:
        chunks = json.load(f)
        
    encoding = tiktoken.get_encoding("cl100k_base")
    
    results = {
        "total_chunks": len(chunks),
        "passed": 0,
        "failed": 0,
        "issues": []
    }
    
    for chunk in chunks:
        chunk_id = chunk.get("chunk_id", "unknown")
        issues = []
        
        # Token count check
        text = chunk.get("content", "")
        token_count = len(encoding.encode(text))
        
        # Strict upper limit check, soft lower limit check
        if token_count > 512:
            issues.append(f"Token count {token_count} exceeds 512 limit")
        
        # Metadata presence
        if "department" not in chunk:
            issues.append("Missing department field")
        
        if "accessible_roles" not in chunk:
            issues.append("Missing accessible_roles field")
        elif not chunk["accessible_roles"]:
             issues.append("Empty accessible_roles list")
             
        if not text.strip():
            issues.append("Empty content")
            
        if issues:
            results["failed"] += 1
            results["issues"].append({
                "chunk_id": chunk_id,
                "issue_type": "Validation Failed",
                "details": issues
            })
        else:
            results["passed"] += 1
            
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=2)
        
    print(f"Validation Complete.")
    print(f"Total: {results['total_chunks']}")
    print(f"Passed: {results['passed']}")
    print(f"Failed: {results['failed']}")
    if results['failed'] > 0:
        print(f"See {output_file} for details.")

if __name__ == "__main__":
    run_validation()
