"""
AI Menu Assistant using LLM and RAG
"""

from langchain_ollama.llms import OllamaLLM
from ai.rag_engine import get_rag_engine
from ai.prompts import menu_assistant_prompt_tr, menu_assistant_prompt_en, get_welcome_message
import os
from dotenv import load_dotenv

load_dotenv()


class MenuAssistant:
    """AI Assistant for menu recommendations and queries"""
    
    def __init__(self):
        self.model_name = os.getenv('OLLAMA_MODEL', 'llama3.2')
        self.llm = OllamaLLM(model=self.model_name, num_predict=150, temperature=0.7)
        self.rag_engine = get_rag_engine()
        # Keep both chains
        self.chain_tr = menu_assistant_prompt_tr | self.llm
        self.chain_en = menu_assistant_prompt_en | self.llm
    
    def get_response(self, question, language='tr', filters=None):
        """
        Get AI response to user question
        
        Args:
            question: User's question
            language: 'tr' or 'en'
            filters: Optional filters for menu search
        
        Returns:
            AI response string
        """
        try:
            # Search relevant menu items using RAG
            menu_docs = self.rag_engine.get_recommendations(question, filters)
            
            # Format menu items for prompt
            menu_items_text = self._format_menu_items(menu_docs, language)
            
            # Select the appropriate chain based on language
            chain = self.chain_tr if language == 'tr' else self.chain_en
            
            # Generate response
            response = chain.invoke({
                "menu_items": menu_items_text,
                "question": question
            })
            
            return response
            
        except Exception as e:
            print(f"Error generating response: {e}")
            return self._get_error_message(language)
    
    def _format_menu_items(self, docs, language='tr'):
        """Format retrieved documents for prompt with item IDs"""
        if not docs:
            if language == 'tr':
                return "Menüde bu kriterlere uygun ürün bulunamadı. Lütfen mevcut kategorilerimizden seçim yapın."
            else:
                return "No items found matching these criteria. Please choose from our available categories."
        
        # Collect unique categories
        categories = set()
        for doc in docs:
            cat = doc.metadata.get('category', 'N/A')
            if cat != 'N/A':
                categories.add(cat)
        
        formatted = []
        
        # Add category info at the beginning
        if categories:
            cat_list = ", ".join(sorted(categories))
            if language == 'tr':
                formatted.append(f"📋 Bulunan kategoriler: {cat_list}\n")
            else:
                formatted.append(f"📋 Found categories: {cat_list}\n")
        
        for i, doc in enumerate(docs, 1):
            metadata = doc.metadata
            item_id = metadata.get('item_id', 'N/A')
            
            if language == 'tr':
                item_text = f"""
{i}. {metadata.get('name', 'Unknown')} (ID: {item_id})
   - Kategori: {metadata.get('category', 'N/A')}
   - Fiyat: {metadata.get('price', 0)} TL
   - Açıklama: {doc.page_content[:200]}
"""
            else:
                item_text = f"""
{i}. {metadata.get('name', 'Unknown')} (ID: {item_id})
   - Category: {metadata.get('category', 'N/A')}
   - Price: {metadata.get('price', 0)} TL
   - Description: {doc.page_content[:200]}
"""
            formatted.append(item_text)
        
        return "\n".join(formatted)
    
    def _get_error_message(self, language='tr'):
        """Get error message"""
        if language == 'tr':
            return """
😔 Üzgünüm, şu anda bir teknik sorun yaşıyorum. 

Lütfen:
- Sorunuzu yeniden ifade edin
- Veya menüden direkt seçim yapın
- Personelimizden yardım isteyin

Anlayışınız için teşekkürler! 🙏
"""
        else:
            return """
😔 Sorry, I'm experiencing a technical issue right now.

Please:
- Rephrase your question
- Or select directly from the menu
- Ask our staff for help

Thank you for understanding! 🙏
"""
    
    def get_item_recommendation(self, preferences):
        """
        Get recommendations based on user preferences
        
        Args:
            preferences: Dict with keys like 'vegetarian', 'spicy', 'budget', etc.
        
        Returns:
            List of recommended item IDs
        """
        query_parts = []
        
        if preferences.get('vegetarian'):
            query_parts.append("vejetaryen")
        if preferences.get('vegan'):
            query_parts.append("vegan")
        if preferences.get('spicy'):
            query_parts.append("acılı")
        if preferences.get('budget'):
            query_parts.append(f"{preferences['budget']} TL altında")
        
        query = " ".join(query_parts) if query_parts else "popüler ürünler"
        
        docs = self.rag_engine.search_menu(query)
        return [doc.metadata.get('item_id') for doc in docs if doc.metadata.get('item_id')]
    
    def check_allergens(self, item_name, user_allergens):
        """
        Check if item is safe for user with allergies
        
        Args:
            item_name: Name of the menu item
            user_allergens: List of allergens to check
        
        Returns:
            (is_safe: bool, message: str)
        """
        # Search for the specific item
        docs = self.rag_engine.search_menu(item_name, k=1)
        
        if not docs:
            return False, "Ürün bulunamadı."
        
        item = docs[0]
        item_allergens = item.metadata.get('allergens', '').lower()
        
        # Check each allergen
        found_allergens = []
        for allergen in user_allergens:
            if allergen.lower() in item_allergens:
                found_allergens.append(allergen)
        
        if found_allergens:
            return False, f"⚠️ Bu üründe {', '.join(found_allergens)} içeriği bulunmaktadır!"
        else:
            return True, "✅ Bu ürün belirttiğiniz alerjenler açısından güvenlidir."
    
    def get_welcome_message(self, language='tr'):
        """Get welcome message"""
        return get_welcome_message(language)


# Global instance
_assistant = None

def get_assistant():
    """Get or create assistant instance"""
    global _assistant
    if _assistant is None:
        _assistant = MenuAssistant()
    return _assistant


if __name__ == "__main__":
    # Test the assistant
    assistant = get_assistant()
    
    print("🤖 Testing Menu Assistant...")
    print("\n" + "="*50)
    
    test_questions = [
        "Vejetaryen pizzanız var mı?",
        "En ucuz yemek ne?",
        "Çocuklar için ne önerirsiniz?"
    ]
    
    for question in test_questions:
        print(f"\n❓ Soru: {question}")
        print(f"\n🤖 Cevap:\n{assistant.get_response(question)}")
        print("\n" + "="*50)
