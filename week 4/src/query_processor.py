import json
import os
import re

class QueryProcessor:
    def __init__(self):
        base_dir = os.path.dirname(os.path.abspath(__file__))
        config_path = os.path.join(base_dir, '..', 'config', 'synonyms.json')
        
        with open(config_path, 'r', encoding='utf-8') as f:
            self.config = json.load(f)
            
        self.abbreviations = self.config.get("abbr", {})
        self.synonyms = self.config.get("synonyms", {})

    def preprocess(self, query):
        if not query: return ""
        
        # 1. Lowercase
        query = query.lower()
        
        # 2. Basic cleanup (keep alphanumeric + spaces + basic punctuation)
        query = re.sub(r'[^\w\s\?\.,]', '', query)
        
        # 3. Expand Abbreviations
        words = query.split()
        expanded_words = []
        for word in words:
            # check if simple match
            if word in self.abbreviations:
                expanded_words.append(self.abbreviations[word])
            else:
                expanded_words.append(word)
        
        processed_query = " ".join(expanded_words)
        
        # 4. (Optional) Synonym expansion could be added, e.g. appending synonyms to query
        # But this might drift semantic meaning if not careful.
        # For now, we return the cleaner, expanded query.
        
        return processed_query

    def extract_keywords(self, query):
        # Naive keyword extraction (removing stop words could be added)
        # For this task, just basic splitting
        return query.lower().split()

if __name__ == "__main__":
    qp = QueryProcessor()
    q = "What is the Q4 ROI?"
    print(f"Original: {q}")
    print(f"Processed: {qp.preprocess(q)}")
