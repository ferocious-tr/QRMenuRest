"""
Test AI Assistant Improvements
Tests the new product recommendation and cart integration features
"""

from ai.assistant import get_assistant
from utils.ai_helper import parse_ai_response_for_products
from database.db_manager import get_db

def test_ai_response_with_products():
    """Test if AI returns product IDs in responses"""
    print("="*60)
    print("Testing AI Assistant Product Recommendations")
    print("="*60)
    print()
    
    # Initialize assistant
    print("🤖 Initializing AI Assistant...")
    assistant = get_assistant()
    print("✅ Assistant initialized")
    print()
    
    # Test questions
    test_questions = [
        ("Vejetaryen pizza önerir misin?", "tr"),
        ("What vegetarian pizzas do you have?", "en"),
        ("100 TL altında ne var?", "tr"),
    ]
    
    for question, lang in test_questions:
        print(f"📝 Question ({lang}): {question}")
        print("-" * 60)
        
        try:
            # Get AI response
            response = assistant.get_response(question, language=lang)
            print(f"🤖 AI Response:\n{response}\n")
            
            # Parse for product IDs
            product_ids, clean_text = parse_ai_response_for_products(response)
            
            if product_ids:
                print(f"✅ Found {len(product_ids)} product IDs: {product_ids}")
                print(f"📄 Clean text:\n{clean_text[:200]}...\n")
                
                # Get actual products
                db = get_db()
                print("🍽️  Products:")
                for pid in product_ids:
                    product = db.get_menu_item(pid)
                    if product:
                        print(f"  - [{pid}] {product.name} - {product.price} TL")
                    else:
                        print(f"  - [{pid}] ⚠️  Product not found in database")
                db.close()
            else:
                print("⚠️  No product IDs found in response")
                print("💡 Tip: Make sure RAG engine has item_id in metadata")
            
        except Exception as e:
            print(f"❌ Error: {e}")
        
        print()
        print("="*60)
        print()

def test_welcome_messages():
    """Test if welcome messages are loaded from database"""
    print("="*60)
    print("Testing Database-Driven Welcome Messages")
    print("="*60)
    print()
    
    from ai.prompts import get_welcome_message
    
    # Test Turkish
    print("🇹🇷 Turkish Welcome Message:")
    print("-" * 60)
    welcome_tr = get_welcome_message('tr')
    print(welcome_tr)
    print()
    
    # Test English
    print("🇬🇧 English Welcome Message:")
    print("-" * 60)
    welcome_en = get_welcome_message('en')
    print(welcome_en)
    print()

def test_helper_functions():
    """Test helper functions"""
    print("="*60)
    print("Testing Helper Functions")
    print("="*60)
    print()
    
    from utils.ai_helper import extract_product_ids_from_response, format_product_for_chat
    
    # Test extraction
    test_text = "**Margherita Pizza** [PRODUCT:5] harika bir seçim! Ayrıca **Caesar Salad** [PRODUCT:12] de deneyebilirsiniz."
    print(f"📝 Test text:\n{test_text}\n")
    
    ids = extract_product_ids_from_response(test_text)
    print(f"✅ Extracted IDs: {ids}\n")
    
    # Test formatting
    db = get_db()
    product = db.get_menu_item(1)
    if product:
        formatted = format_product_for_chat(product, 'tr')
        print(f"📄 Formatted product:\n{formatted}\n")
    else:
        print("⚠️  No product found with ID 1\n")
    db.close()

if __name__ == "__main__":
    print("\n")
    print("🧪 AI ASSISTANT IMPROVEMENTS TEST SUITE")
    print("="*60)
    print()
    
    try:
        # Test 1: Welcome Messages
        test_welcome_messages()
        input("Press Enter to continue to next test...")
        print("\n")
        
        # Test 2: Helper Functions
        test_helper_functions()
        input("Press Enter to continue to next test...")
        print("\n")
        
        # Test 3: AI Responses (requires vector DB and Ollama)
        print("⚠️  Note: This test requires Ollama to be running")
        response = input("Continue? (y/n): ")
        if response.lower() == 'y':
            test_ai_response_with_products()
        
        print("\n")
        print("="*60)
        print("✅ ALL TESTS COMPLETED!")
        print("="*60)
        
    except KeyboardInterrupt:
        print("\n\n⚠️  Tests interrupted by user")
    except Exception as e:
        print(f"\n\n❌ Test suite failed: {e}")
        import traceback
        traceback.print_exc()
