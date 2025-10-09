"""
Test AI Model Configuration
"""

import os
from dotenv import load_dotenv
from langchain_ollama.llms import OllamaLLM

# Load environment
load_dotenv()

def test_model_config():
    """Test if AI model is properly configured"""
    
    print("=" * 70)
    print("AI Model Configuration Test")
    print("=" * 70)
    print()
    
    # Get model name from .env
    model_name = os.getenv('OLLAMA_MODEL', 'llama3.2')
    embedding_model = os.getenv('EMBEDDING_MODEL', 'mxbai-embed-large')
    
    print("📋 Configuration from .env:")
    print(f"   OLLAMA_MODEL: {model_name}")
    print(f"   EMBEDDING_MODEL: {embedding_model}")
    print()
    
    # Test Turkish prompt
    print("🇹🇷 Testing Turkish language response...")
    try:
        llm = OllamaLLM(model=model_name)
        
        turkish_test = """
Sen bir restoran asistanısın. TÜRKÇE yanıt ver.

Soru: Merhaba, vejetaryen pizzanız var mı?

Cevap:"""
        
        print("   Sending test prompt...")
        response_tr = llm.invoke(turkish_test)
        print(f"\n   ✅ Turkish Response:\n   {response_tr[:200]}...")
        print()
        
    except Exception as e:
        print(f"   ❌ Error: {e}")
        print()
    
    # Test English prompt
    print("🇬🇧 Testing English language response...")
    try:
        llm = OllamaLLM(model=model_name)
        
        english_test = """
You are a restaurant assistant. RESPOND IN ENGLISH.

Question: Hello, do you have vegetarian pizza?

Answer:"""
        
        print("   Sending test prompt...")
        response_en = llm.invoke(english_test)
        print(f"\n   ✅ English Response:\n   {response_en[:200]}...")
        print()
        
    except Exception as e:
        print(f"   ❌ Error: {e}")
        print()
    
    print("=" * 70)
    print("Test completed!")
    print("=" * 70)

if __name__ == "__main__":
    test_model_config()
