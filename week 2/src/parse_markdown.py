import os
import json
import glob
import re

def parse_markdown_files():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    input_dir = os.path.join(base_dir, '..', '..', 'week 1', 'data')
    output_dir = os.path.join(base_dir, '..', 'output')
    output_file = os.path.join(output_dir, 'parsed_markdown.json')
    
    os.makedirs(output_dir, exist_ok=True)
    
    parsed_data = []
    
    search_pattern = os.path.join(input_dir, "**", "*.md")
    files = glob.glob(search_pattern, recursive=True)
    
    print(f"Parsing {len(files)} markdown files...")
    
    for file_path in files:
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Extract title (first # heading)
            title_match = re.search(r'^#\s+(.+)$', content, re.MULTILINE)
            title = title_match.group(1).strip() if title_match else "Untitled"
            
            # Extract section headings (##)
            sections = re.findall(r'^##\s+(.+)$', content, re.MULTILINE)
            
            # Determine department from folder structure
            # Path might be .../week 1/data/Finance/somefile.md
            rel_path = os.path.relpath(file_path, input_dir)
            parts = rel_path.split(os.sep)
            department = parts[0] if len(parts) > 0 else "Unknown"
            
            parsed_data.append({
                "filename": os.path.basename(file_path),
                "full_file_path": os.path.abspath(file_path),
                "title": title,
                "section_headings": sections,
                "content": content,
                "department": department
            })
            print(f"Parsed: {os.path.basename(file_path)}")
            
        except Exception as e:
            print(f"Error parsing {file_path}: {e}")
            
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(parsed_data, f, indent=2)
        
    print(f"Saved parsed data to {output_file}")

if __name__ == "__main__":
    parse_markdown_files()
