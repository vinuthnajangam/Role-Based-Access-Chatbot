import sys
import os
import json
from openai import OpenAI
from dotenv import load_dotenv

# Load env
load_dotenv()

# Paths
base_dir = os.path.dirname(os.path.abspath(__file__))
week4_src = os.path.join(base_dir, '..', '..', 'week 4', 'src')
sys.path.append(week4_src)

from search_pipeline import SearchPipeline

class RAGPipeline:
    def __init__(self):
        self.retriever = SearchPipeline()
        
        # Configure LLM Client
        # User requested support for OpenRouter or similar
        self.api_key = os.getenv("LLM_API_KEY")
        self.base_url = os.getenv("LLM_BASE_URL", "https://openrouter.ai/api/v1")
        self.model_name = os.getenv("LLM_MODEL", "mistralai/mistral-7b-instruct")
        
        if self.api_key:
            print(f"RAG Initialized with LLM: {self.model_name}")
            self.client = OpenAI(
                api_key=self.api_key,
                base_url=self.base_url
            )
        else:
            print("RAG Initialized in Offline Mode (No API Key found)")
            self.client = None

    def generate_response(self, query, user_role, stream=False):
        # 1. Retrieve Context
        search_result = self.retriever.search(query, user_role)
        results = search_result['results']
        
        # 2. Build Context String
        context_text = ""
        sources = []
        for i, res in enumerate(results):
            content = res['content'].replace("\n", " ")
            dept = res['metadata'].get('department', 'Unknown')
            context_text += f"\n[Doc {i+1} - {dept}]: {content}\n"
            sources.append(res)
            
        # 3. Construct Prompt with Role-Based Access Control
        role_context = {
            "c-level": "ALL departments (Finance, HR, Marketing, Engineering, General)",
            "finance": "ONLY Finance department",
            "hr": "ONLY HR department", 
            "marketing": "ONLY Marketing department",
            "engineering": "ONLY Engineering department",
            "employees": "ONLY General company information"
        }
        
        access_scope = role_context.get(user_role.lower(), "General information")
        is_admin = user_role.lower() == "c-level"
        
        # Different prompts for Admin vs regular users
        if is_admin:
            # Admin has unrestricted access - no department boundaries
            system_prompt = f"""You are a secure enterprise assistant for an ADMIN user with full access.

ADMIN PRIVILEGES:
- Current User Role: ADMIN (C-Level)
- Access Level: UNRESTRICTED - Full access to ALL departments and information

RULES FOR ADMIN:
1. **Full Access**: Answer ANY question about company information from ANY department.
2. **No Restrictions**: You have access to Finance, HR, Marketing, Engineering, and General information.
3. **Context-Based**: Use the provided context documents to answer questions.
4. **No Context Available**: If no relevant documents found, say:
   "I cannot find this information in the available documents."
5. **Greetings**: For greetings ('Hi', 'Hello'), respond politely: "Hello Admin! I can help you with information from any department. What would you like to know?"
6. **Unrelated Questions**: If question is completely unrelated to company/work (e.g., weather, sports, recipes), say:
   "❌ This question is not related to company information."

REMEMBER: As an admin, you have full access. Answer all company-related questions.
"""
        else:
            # Regular users have strict access control
            system_prompt = f"""You are a secure RBAC-protected enterprise assistant with strict access control.

ROLE-BASED ACCESS CONTROL:
- Current User Role: {user_role.upper()}
- Authorized Access: {access_scope}

STRICT RULES:
1. **Access Control**: Answer ONLY questions related to {access_scope}.
2. **Out-of-Scope Rejection**: If the question is about departments the user CANNOT access, respond with:
   "🚫 Access Denied: You do not have permission to access that department's information. Please ask questions related to {access_scope}."
3. **Context-Only Answers**: Use ONLY the provided context documents. Never use external knowledge.
4. **No Context Available**: If no relevant documents found, say:
   "I cannot find this information in the {access_scope} documents you have access to."
5. **Greetings**: For greetings ('Hi', 'Hello'), respond politely: "Hello! I'm your secure assistant. I can help you with {access_scope}. What would you like to know?"
6. **Unrelated Questions**: If question is completely unrelated to company/work (e.g., weather, sports, recipes), say:
   "❌ This question is not related to company information. Please ask about {access_scope}."

REMEMBER: Strictly enforce access control. Reject unauthorized requests clearly.
"""
        
        user_prompt = f"""
DEPARTMENT CONTEXT DOCUMENTS:
{context_text if context_text.strip() else "[No documents found in authorized departments]"}

USER QUESTION: 
{query}

YOUR ANSWER (following all rules above):
"""
        
        # 4. Call LLM or Fallback
        generated_text = ""
        
        if self.client:
            try:
                completion = self.client.chat.completions.create(
                    model=self.model_name,
                    messages=[
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": user_prompt}
                    ]
                )
                generated_text = completion.choices[0].message.content
            except Exception as e:
                generated_text = f"Error generating response: {str(e)}"
        else:
            if not results:
                generated_text = "I couldn't find any relevant documents. (AI Generation is disabled)"
            else:
                generated_text = "Detailed AI response is disabled (No API Key). Here are the documents found:"

        return {
            "query": query,
            "response": generated_text,
            "results": sources,
            "metrics": {
                "documents_retrieved": len(sources),
                "avg_similarity": round(sum([1 - r.get('score', 0.5) for r in sources]) / max(len(sources), 1), 3),
                "llm_enabled": self.client is not None,
                "model": self.model_name if self.client else None,
                "context_tokens": len(context_text.split())
            }
        }

if __name__ == "__main__":
    rag = RAGPipeline()
    # Mock test if key exists
    if os.getenv("LLM_API_KEY"):
        print(rag.generate_response("Q4 revenue", "finance"))
