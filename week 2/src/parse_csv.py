import os
import json
import glob
import pandas as pd

def parse_csv_files():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    input_dir = os.path.join(base_dir, '..', '..', 'week 1', 'data')
    output_dir = os.path.join(base_dir, '..', 'output')
    output_file = os.path.join(output_dir, 'parsed_csv.json')
    
    os.makedirs(output_dir, exist_ok=True)
    
    parsed_data = []
    
    search_pattern = os.path.join(input_dir, "**", "*.csv")
    files = glob.glob(search_pattern, recursive=True)
    
    print(f"Parsing {len(files)} CSV files...")
    
    for file_path in files:
        try:
            # Use pandas to read
            # Try utf-8 first, then fallback or ignore errors as per prompt hint "encoding_errors='ignore'"
            try:
                df = pd.read_csv(file_path, encoding='utf-8')
            except UnicodeDecodeError:
                 df = pd.read_csv(file_path, encoding_errors='ignore')

            columns = df.columns.tolist()
            
            # Convert rows to text format
            text_lines = []
            for _, row in df.iterrows():
                row_str = "; ".join([f"{col}: {row[col]}" for col in columns])
                text_lines.append(row_str)
            
            text_content = "\n".join(text_lines)
            
            # Determine department
            rel_path = os.path.relpath(file_path, input_dir)
            parts = rel_path.split(os.sep)
            department = parts[0] if len(parts) > 0 else "Unknown"
            
            parsed_data.append({
                "filename": os.path.basename(file_path),
                "filepath": os.path.abspath(file_path),
                "department": department,
                "columns": columns,
                "row_count": len(df),
                "text_content": text_content
            })
            
            print(f"Processed: {os.path.basename(file_path)} ({len(df)} rows)")
            
        except Exception as e:
            print(f"Error parsing {file_path}: {e}")
            
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(parsed_data, f, indent=2)
        
    print(f"Saved parsed CSV data to {output_file}")

if __name__ == "__main__":
    parse_csv_files()
