import os
import json
import unicodedata
import re

def detailed_clean(text):
    if not text:
        return ""
    text = unicodedata.normalize('NFKC', text)
    # Remove special characters except basic punctuation (.,!?;:-)
    # [^\w\s.,!?;:-] removes anything that is NOT word, whitespace, or punctuation.
    text = re.sub(r'[^\w\s.,!?;:-]', '', text)
    
    # Normalize newlines: multiple newlines -> double newline
    # Collapse 3 or more newlines into 2
    text = re.sub(r'\n{3,}', '\n\n', text)
    
    lines = text.split('\n')
    cleaned_lines = []
    for line in lines:
        # replace multiple spaces with single space
        line = re.sub(r'[ \t]+', ' ', line)
        cleaned_lines.append(line.strip())
        
    text = '\n'.join(cleaned_lines)
    # Fix potential multi-newlines again after strip
    text = re.sub(r'\n{3,}', '\n\n', text)
    
    return text.strip()

def process_cleaning():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    output_dir = os.path.join(base_dir, '..', 'output')
    
    md_file = os.path.join(output_dir, 'parsed_markdown.json')
    csv_file = os.path.join(output_dir, 'parsed_csv.json')
    output_file = os.path.join(output_dir, 'cleaned_documents.json')
    
    if not os.path.exists(md_file) or not os.path.exists(csv_file):
        print("Input files not found. Run parsing scripts first.")
        return

    with open(md_file, 'r', encoding='utf-8') as f:
        md_data = json.load(f)
        
    with open(csv_file, 'r', encoding='utf-8') as f:
        csv_data = json.load(f)
        
    cleaned_docs = []
    total_chars_removed = 0
    
    # Process Markdown
    for doc in md_data:
        original = doc.get("content", "")
        cleaned = detailed_clean(original)
        
        removed = len(original) - len(cleaned)
        total_chars_removed += removed
        
        cleaned_docs.append({
            "id": doc.get("filename"), # Use filename as ID 
            "source_type": "markdown",
            "filename": doc.get("filename"),
            "department": doc.get("department"),
            "cleaned_content": cleaned,
            "original_length": len(original),
            "cleaned_length": len(cleaned),
            "full_path": doc.get("full_file_path")
        })
        
    # Process CSV
    for doc in csv_data:
        original = doc.get("text_content", "")
        cleaned = detailed_clean(original)
        
        removed = len(original) - len(cleaned)
        total_chars_removed += removed
        
        cleaned_docs.append({
            "id": doc.get("filename"),
            "source_type": "csv",
            "filename": doc.get("filename"),
            "department": doc.get("department"),
            "cleaned_content": cleaned,
            "original_length": len(original),
            "cleaned_length": len(cleaned),
            "full_path": doc.get("filepath")
        })
        
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(cleaned_docs, f, indent=2)
        
    print(f"Total docs: {len(cleaned_docs)}")
    print(f"Characters removed: {total_chars_removed}")
    print(f"Saved to {output_file}")

if __name__ == "__main__":
    process_cleaning()
