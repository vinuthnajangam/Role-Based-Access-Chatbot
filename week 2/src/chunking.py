import os
import json
import glob
import tiktoken
from langchain_text_splitters import RecursiveCharacterTextSplitter

def process_documents():
    # Setup paths
    base_dir = os.path.dirname(os.path.abspath(__file__))
    input_dir = os.path.join(base_dir, '..', '..', 'week 1', 'data')
    output_dir = os.path.join(base_dir, '..', 'output')
    output_file = os.path.join(output_dir, 'chunked_documents.json')
    
    os.makedirs(output_dir, exist_ok=True)
    
    # Initialize tokenizer and splitter
    # Using 'cl100k_base' which is used by GPT-4 and GPT-3.5
    encoding = tiktoken.get_encoding("cl100k_base")
    
    # Text splitter setup
    # We want chunks of 300-512 tokens. 
    # RecursiveCharacterTextSplitter operates on characters by default, but we can use from_tiktoken_encoder.
    text_splitter = RecursiveCharacterTextSplitter.from_tiktoken_encoder(
        model_name="gpt-4",
        chunk_size=512,
        chunk_overlap=50
    )
    
    # Find all markdown files
    search_pattern = os.path.join(input_dir, "**", "*.md")
    files = glob.glob(search_pattern, recursive=True)
    
    print(f"Found {len(files)} markdown files in {input_dir}")
    
    chunked_data = []
    chunk_count = 0
    
    for file_path in files:
        print(f"Processing: {file_path}")
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Split into chunks
            chunks = text_splitter.split_text(content)
            
            for chunk_text in chunks:
                chunk_count += 1
                chunk_id = f"chunk_{chunk_count:04d}"
                token_count = len(encoding.encode(chunk_text))
                
                chunked_data.append({
                    "chunk_id": chunk_id,
                    "content": chunk_text,
                    "source_file": os.path.abspath(file_path),
                    "token_count": token_count
                })
                
        except Exception as e:
            print(f"Error processing {file_path}: {e}")
            
    # Save output
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(chunked_data, f, indent=2)
        
    print(f"Successfully created {len(chunked_data)} chunks. Saved to {output_file}")

if __name__ == "__main__":
    process_documents()
