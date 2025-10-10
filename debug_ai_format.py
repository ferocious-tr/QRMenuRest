"""
Debug AI Response Format
Check if AI is using [PRODUCT:ID] format correctly
"""

from ai.assistant import get_assistant

def test_ai_format():
    """Test AI response format"""
    print("="*60)
    print("Testing AI Response Format")
    print("="*60)
    print()
    
    assistant = get_assistant()
    
    # Simple test question
    question = "Kahvaltı ne önerirsin?"
    print(f"Question: {question}")
    print("-"*60)
    
    try:
        response = assistant.get_response(question, language='tr')
        
        print("Raw AI Response:")
        print("="*60)
        print(response)
        print("="*60)
        print()
        
        # Check format
        if "[PRODUCT:" in response:
            print("✅ Contains [PRODUCT:ID] format")
        else:
            print("❌ Missing [PRODUCT:ID] format")
            print("💡 AI should include [PRODUCT:ID] after each recommendation")
        
        # Check if it's just a list
        if response.strip().startswith("[") and response.strip().endswith("]"):
            print("⚠️  AI returned a plain list instead of formatted text")
            print("💡 Check AI prompt template")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_ai_format()
