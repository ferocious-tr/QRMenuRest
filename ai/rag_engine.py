"""
RAG Engine for Menu AI Assistant
Adapts existing vector.py for menu recommendation system
"""

from langchain_ollama import OllamaEmbeddings
from langchain_chroma import Chroma
from langchain_core.documents import Document
import os
import pandas as pd
from dotenv import load_dotenv

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
        """Create vector documents from menu data"""
        documents = []
        ids = []
        
        # Load menu items from CSV
        try:
            df = pd.read_csv("data/menu_items.csv")
            
            for i, row in df.iterrows():
                # Create rich document with all menu information
                content = self._create_document_content(row)
                
                document = Document(
                    page_content=content,
                    metadata={
                        "item_id": i + 1,
                        "name": row["Name"],
                        "name_en": row["Name_EN"],
                        "category": row["Category"],
                        "price": row["Price"],
                        "is_vegetarian": row["Is_Vegetarian"],
                        "is_vegan": row["Is_Vegan"],
                        "is_spicy": row["Is_Spicy"],
                        "allergens": row["Allergens"],
                    },
                    id=str(i + 1)
                )
                documents.append(document)
                ids.append(str(i + 1))
            
            print(f"✅ Created {len(documents)} menu documents")
            
        except Exception as e:
            print(f"⚠️  Error loading menu data: {e}")
            print("💡 Using reviews data as fallback...")
            # Fallback to old review data
            df = pd.read_csv("realistic_restaurant_reviews.csv")
            for i, row in df.iterrows():
                document = Document(
                    page_content=row["Title"] + " " + row["Review"],
                    metadata={"rating": row["Rating"], "date": row["Date"]},
                    id=str(i)
                )
                documents.append(document)
                ids.append(str(i))
        
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
    
    def _create_document_content(self, row):
        """Create rich text content for embedding"""
        content_parts = [
            f"Yemek Adı: {row['Name']} ({row['Name_EN']})",
            f"Kategori: {row['Category']}",
            f"Açıklama: {row['Description']}",
            f"Fiyat: {row['Price']} TL",
        ]
        
        if row['Is_Vegetarian']:
            content_parts.append("Vejetaryen uyumlu")
        if row['Is_Vegan']:
            content_parts.append("Vegan uyumlu")
        if row['Is_Spicy']:
            content_parts.append(f"Acılık seviyesi: {row['Spicy_Level']}/5")
        
        if pd.notna(row['Allergens']) and row['Allergens']:
            content_parts.append(f"Alerjenler: {row['Allergens']}")
        
        if pd.notna(row['Ingredients']) and row['Ingredients']:
            content_parts.append(f"İçindekiler: {row['Ingredients']}")
        
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
