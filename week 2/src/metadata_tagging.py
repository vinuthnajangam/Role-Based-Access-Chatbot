import os
import json

def process_metadata_tagging():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    input_file = os.path.join(base_dir, '..', 'output', 'chunked_documents.json')
    config_file = os.path.join(base_dir, '..', 'config', 'role_mappings.json')
    output_file = os.path.join(base_dir, '..', 'output', 'tagged_chunks.json')
    
    if not os.path.exists(input_file):
        print("Input file chunked_documents.json not found.")
        return

    with open(input_file, 'r', encoding='utf-8') as f:
        chunks = json.load(f)
        
    with open(config_file, 'r', encoding='utf-8') as f:
        config = json.load(f)
        
    dept_mappings = config.get("departments", {})
    # Lowercase keys for reliable matching
    dept_mappings_lower = {k.lower(): v for k, v in dept_mappings.items()}
    
    tagged_chunks = []
    stats = {}
    
    for chunk in chunks:
        source_path = chunk.get("source_file", "")
        # Try to detect department from path
        # Assume path contains department name folder (e.g. .../Finance/...)
        # Also check content keywords if path fails? 
        # The prompt says: "Detect department from source_file path OR keywords in content"
        
        detected_dept = None
        
        # 1. Path detection
        norm_path = source_path.replace('\\', '/').split('/')
        for dept_name in dept_mappings.keys():
            if dept_name in norm_path or dept_name.lower() in [p.lower() for p in norm_path]:
                detected_dept = dept_name
                break
        
        # 2. Keyword detection (if path failed or is ambiguous)
        if not detected_dept:
             content_lower = chunk.get("content", "").lower()
             keywords_map = config.get("keywords", {})
             for dept_key, keywords in keywords_map.items():
                 for kw in keywords:
                     if kw in content_lower:
                         # map dept_key back to dept_mappings key
                         # finding case-insensitive match in dept_mappings keys
                         for valid_dept in dept_mappings.keys():
                             if valid_dept.lower() == dept_key.lower():
                                 detected_dept = valid_dept
                                 break
                         if detected_dept: break
                 if detected_dept: break

        if not detected_dept:
            detected_dept = "general" # Fallback

        # Assign roles
        roles = dept_mappings_lower.get(detected_dept.lower(), [])
        
        # Add metadata
        chunk['department'] = detected_dept
        chunk['accessible_roles'] = roles
        chunk['source'] = os.path.basename(source_path)
        
        tagged_chunks.append(chunk)
        
        # Stats
        stats[detected_dept] = stats.get(detected_dept, 0) + 1
        
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(tagged_chunks, f, indent=2)
        
    print("Tagging complete.")
    for dept, count in stats.items():
        print(f"{dept}: {count} chunks")
        
    print(f"Saved to {output_file}")

if __name__ == "__main__":
    process_metadata_tagging()
