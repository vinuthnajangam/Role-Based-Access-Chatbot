"""
API Key Tester - Test your LLM API keys before using them
Usage: python test_api_key.py
"""

import os
from dotenv import load_dotenv
from openai import OpenAI

# Load environment variables
load_dotenv()

def test_api_key():
    """Test if the configured API key works"""
    
    api_key = os.getenv("LLM_API_KEY")
    base_url = os.getenv("LLM_BASE_URL", "https://openrouter.ai/api/v1")
    model = os.getenv("LLM_MODEL", "deepseek/deepseek-r1:free")
    
    print("=" * 50)
    print("🔑 API KEY TESTER")
    print("=" * 50)
    print(f"\n📌 Configuration:")
    print(f"   Base URL: {base_url}")
    print(f"   Model: {model}")
    print(f"   API Key: {api_key[:20]}..." if api_key else "   API Key: NOT SET")
    print()
    
    if not api_key:
        print("❌ ERROR: No API key found in .env file!")
        print("   Please add LLM_API_KEY to your .env file")
        return False
    
    try:
        print("🔄 Testing connection...")
        
        client = OpenAI(
            api_key=api_key,
            base_url=base_url
        )
        
        # Simple test message
        response = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "user", "content": "Say 'Hello, the API is working!' in exactly those words."}
            ],
            max_tokens=50
        )
        
        reply = response.choices[0].message.content
        
        print("\n✅ SUCCESS! API is working!")
        print(f"\n📨 Test Response:")
        print(f"   {reply}")
        print("\n" + "=" * 50)
        print("Your API key is valid. The chatbot should work now!")
        print("=" * 50)
        return True
        
    except Exception as e:
        error_msg = str(e)
        print(f"\n❌ FAILED! Error occurred:")
        print(f"   {error_msg}")
        
        # Provide helpful suggestions based on error
        if "401" in error_msg:
            print("\n💡 Fix: Your API key is invalid or expired.")
            print("   Get a new key from: https://openrouter.ai/keys")
        elif "429" in error_msg:
            print("\n💡 Fix: Rate limit exceeded. Wait a few minutes and try again.")
        elif "404" in error_msg:
            print("\n💡 Fix: Model not found. Try a different model.")
        elif "Network" in error_msg or "Connection" in error_msg:
            print("\n💡 Fix: Check your internet connection.")
        
        print("\n" + "=" * 50)
        return False

def test_custom_key(api_key, base_url="https://openrouter.ai/api/v1", model="deepseek/deepseek-r1:free"):
    """Test a custom API key without .env"""
    
    print("=" * 50)
    print("🔑 TESTING CUSTOM API KEY")
    print("=" * 50)
    print(f"\n📌 Testing with:")
    print(f"   Base URL: {base_url}")
    print(f"   Model: {model}")
    print(f"   API Key: {api_key[:20]}...")
    print()
    
    try:
        print("🔄 Testing connection...")
        
        client = OpenAI(api_key=api_key, base_url=base_url)
        
        response = client.chat.completions.create(
            model=model,
            messages=[{"role": "user", "content": "Say 'API works!' only."}],
            max_tokens=20
        )
        
        reply = response.choices[0].message.content
        print(f"\n✅ SUCCESS! Response: {reply}")
        return True
        
    except Exception as e:
        print(f"\n❌ FAILED: {e}")
        return False


if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1:
        # Test custom key passed as argument
        custom_key = sys.argv[1]
        test_custom_key(custom_key)
    else:
        # Test key from .env file
        test_api_key()
