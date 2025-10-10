"""
RAG Engine for Menu AI Assistant
Uses database instead of CSV files for menu data
"""

from langchain_ollama import OllamaEmbeddings
from langchain_chroma import Chroma
from langchain_core.documents import Document
import os
from dotenv import load_dotenv
from database.db_manager import get_db

load_dotenv()

class MenuRAGEngine:
    """RAG Engine specifically for menu recommendations"""
    
    def __init__(self):
        self.embedding_model = os.getenv('EMBEDDING_MODEL', 'mxbai-embed-large')
        self.db_location = os.getenv('VECTOR_DB_PATH', './chrome_langchain_db')
        
        # Initialize embeddings
        self.embeddings = OllamaEmbeddings(model=self.embedding_model)
        
        # Initialize or load vector store
        self.vector_store = None
        self.retriever = None
        self._init_vector_store()
    
    def _init_vector_store(self):
        """Initialize or load vector store"""
        add_documents = not os.path.exists(self.db_location)
        
        if add_documents:
            print("📚 Creating new vector database for menu...")
            self._create_menu_documents()
        else:
            print("📂 Loading existing vector database...")
            self.vector_store = Chroma(
                collection_name="restaurant_menu",
                persist_directory=self.db_location,
                embedding_function=self.embeddings
            )
            self.retriever = self.vector_store.as_retriever(search_kwargs={"k": 5})
    
    def _create_menu_documents(self):
        """Create vector documents from database menu items (only available items)"""
        documents = []
        ids = []
        
        # Load menu items from database - ONLY AVAILABLE ITEMS
        try:
            db = get_db()
            menu_items = db.get_all_menu_items(available_only=True)  # Only active/available items
            
            for item in menu_items:
                # Create rich document with all menu information
                content = self._create_document_content_from_db(item)
                
                document = Document(
                    page_content=content,
                    metadata={
                        "item_id": item.id,
                        "name": item.name,
                        "name_en": item.name_en or item.name,
                        "category": item.category.name if item.category else "Uncategorized",
                        "price": float(item.price),
                        "is_vegetarian": item.is_vegetarian,
                        "is_vegan": item.is_vegan,
                        "is_spicy": item.is_spicy,
                        "spicy_level": item.spicy_level if item.is_spicy else 0,
                        "allergens": item.allergens or "",
                        "ingredients": item.ingredients or "",
                        "is_available": True,  # Always True since we filter
                    },
                    id=str(item.id)
                )
                documents.append(document)
                ids.append(str(item.id))
            
            db.close()
            print(f"✅ Created {len(documents)} menu documents from database (available only)")
            
        except Exception as e:
            print(f"❌ Error loading menu data from database: {e}")
            print("💡 Make sure the database is initialized with menu items")
            raise
        
        # Create vector store
        self.vector_store = Chroma(
            collection_name="restaurant_menu",
            persist_directory=self.db_location,
            embedding_function=self.embeddings
        )
        
        # Add documents
        self.vector_store.add_documents(documents=documents, ids=ids)
        
        # Create retriever
        self.retriever = self.vector_store.as_retriever(search_kwargs={"k": 5})
        
        print("✅ Vector database created successfully!")
    
    def _create_document_content_from_db(self, item):
        """Create rich text content for embedding from database MenuItem"""
        content_parts = [
            f"Yemek Adı: {item.name} ({item.name_en or item.name})",
            f"Kategori: {item.category.name if item.category else 'Kategorisiz'}",
            f"Açıklama: {item.description}",
            f"Fiyat: {item.price} TL",
        ]
        
        # Dietary preferences - ÖNEMLİ ÖZELLIKLER
        dietary_features = []
        if item.is_vegetarian:
            dietary_features.append("VEJETERYENlere uygun")
        if item.is_vegan:
            dietary_features.append("VEGANlara uygun")
        
        if dietary_features:
            content_parts.append("ÖZELLİKLER: " + ", ".join(dietary_features))
        
        # Spiciness level
        if item.is_spicy:
            content_parts.append(f"ACILIK: {item.spicy_level}/5 seviyesinde acı")
        
        # Allergens - ÇOK ÖNEMLİ
        if item.allergens:
            content_parts.append(f"⚠️ ALERJENLER: {item.allergens} içerir - alerjisi olanlar dikkat etmeli")
        
        # Ingredients
        if item.ingredients:
            content_parts.append(f"İÇİNDEKİLER: {item.ingredients}")
        
        return " | ".join(content_parts)
    
    def search_menu(self, query, k=5):
        """Search menu items based on query"""
        if not self.retriever:
            return []
        
        results = self.retriever.invoke(query)
        return results
    
    def get_recommendations(self, query, filters=None):
        """
        Get menu recommendations based on query and filters
        
        Args:
            query: User's natural language query
            filters: Dict with filters like {'vegetarian': True, 'max_price': 100}
        
        Returns:
            List of recommended items
        """
        results = self.search_menu(query)
        
        if filters:
            # Apply additional filtering
            filtered_results = []
            for doc in results:
                metadata = doc.metadata
                
                # Check filters
                if filters.get('vegetarian') and not metadata.get('is_vegetarian'):
                    continue
                if filters.get('vegan') and not metadata.get('is_vegan'):
                    continue
                if filters.get('max_price') and metadata.get('price', 999) > filters['max_price']:
                    continue
                if filters.get('exclude_allergens'):
                    allergens = metadata.get('allergens', '')
                    if any(allergen in allergens for allergen in filters['exclude_allergens']):
                        continue
                
                filtered_results.append(doc)
            
            return filtered_results
        
        return results
    
    def rebuild_index(self):
        """Rebuild vector index from scratch"""
        if os.path.exists(self.db_location):
            import shutil
            shutil.rmtree(self.db_location)
        self._init_vector_store()


# Global instance
_rag_engine = None

def get_rag_engine():
    """Get or create RAG engine instance"""
    global _rag_engine
    if _rag_engine is None:
        _rag_engine = MenuRAGEngine()
    return _rag_engine


if __name__ == "__main__":
    # Test the RAG engine
    engine = get_rag_engine()
    
    print("\n🔍 Testing search:")
    results = engine.search_menu("vejetaryen pizza önerisi")
    
    print(f"\nFound {len(results)} results:")
    for i, doc in enumerate(results, 1):
        print(f"\n{i}. {doc.metadata.get('name', 'Unknown')}")
        print(f"   Category: {doc.metadata.get('category', 'Unknown')}")
        print(f"   Price: {doc.metadata.get('price', 0)} TL")
