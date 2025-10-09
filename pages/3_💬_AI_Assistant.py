"""
AI Assistant Page - Chat with AI menu assistant
"""

import streamlit as st
from ai.assistant import get_assistant
from ai.prompts import get_welcome_message
from utils.session_manager import init_session_state, add_chat_message, clear_chat_history, add_to_cart
from utils.page_navigation import show_customer_navigation, hide_default_sidebar
from database.db_manager import get_db

# Page config
st.set_page_config(page_title="AI Asistan", page_icon="💬", layout="wide")

# Hide default sidebar
hide_default_sidebar()

# Initialize session
init_session_state()

# Show customer navigation
show_customer_navigation()

# Custom CSS
st.markdown("""
<style>
    .chat-message {
        padding: 1rem;
        border-radius: 15px;
        margin: 0.5rem 0;
        max-width: 80%;
    }
    .user-message {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        margin-left: auto;
    }
    .assistant-message {
        background: #f0f2f6;
        color: #333;
    }
    .chat-container {
        height: 500px;
        overflow-y: auto;
        padding: 1rem;
        background: white;
        border-radius: 10px;
        border: 2px solid #f0f2f6;
    }
    .suggestion-chip {
        display: inline-block;
        background: #e8eaf6;
        color: #3f51b5;
        padding: 0.5rem 1rem;
        border-radius: 20px;
        margin: 0.3rem;
        cursor: pointer;
        border: 2px solid #c5cae9;
        transition: all 0.2s;
    }
    .suggestion-chip:hover {
        background: #c5cae9;
        transform: translateY(-2px);
    }
</style>
""", unsafe_allow_html=True)

def display_chat_message(role, content):
    """Display a chat message"""
    if role == "user":
        st.markdown(f"""
        <div class="chat-message user-message">
            <strong>👤 Siz:</strong><br>
            {content}
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown(f"""
        <div class="chat-message assistant-message">
            <strong>🤖 AI Asistan:</strong><br>
            {content}
        </div>
        """, unsafe_allow_html=True)

def show_suggestions():
    """Display suggestion chips"""
    st.markdown("### 💡 Örnek Sorular")
    
    suggestions = [
        "Vejetaryen ne var?",
        "En ucuz yemek ne?",
        "Acı pizzalarınız var mı?",
        "100 TL altında ne önerebilirsiniz?",
        "Çocuklar için ne uygun?",
        "Fıstık alerjim var, ne yemeli?",
        "En popüler ürünleriniz neler?",
        "Hafif bir şey yemek istiyorum",
    ]
    
    cols = st.columns(2)
    for idx, suggestion in enumerate(suggestions):
        with cols[idx % 2]:
            if st.button(suggestion, key=f"sug_{idx}", use_container_width=True):
                return suggestion
    
    return None

def extract_menu_items_from_response(response, db):
    """Try to extract menu item names from AI response"""
    # This is a simple implementation - can be improved
    items = db.get_all_menu_items()
    found_items = []
    
    response_lower = response.lower()
    for item in items:
        if item.name.lower() in response_lower:
            found_items.append(item)
    
    return found_items

def main():
    """Main AI assistant page"""
    st.title("💬 AI Menü Asistanı")
    
    # Initialize AI assistant
    assistant = get_assistant()
    
    # Sidebar options
    st.sidebar.markdown("### ⚙️ Ayarlar")
    
    # Language selection
    language = st.sidebar.selectbox(
        "🌐 Dil",
        ["Türkçe", "English"],
        key="ai_language"
    )
    lang_code = 'tr' if language == "Türkçe" else 'en'
    
    # Dietary preferences
    st.sidebar.markdown("### 🥗 Tercihler")
    prefer_vegetarian = st.sidebar.checkbox("Vejetaryen Öner")
    prefer_vegan = st.sidebar.checkbox("Vegan Öner")
    budget = st.sidebar.slider("Bütçe (TL)", 0, 150, 150)
    
    # Allergen warnings
    st.sidebar.markdown("### ⚠️ Alerjenler")
    exclude_allergens = st.sidebar.multiselect(
        "Kaçınılacak Alerjenler",
        ["gluten", "dairy", "nuts", "fish", "egg"],
        key="allergen_select"
    )
    
    # Clear chat button
    if st.sidebar.button("🗑️ Sohbeti Temizle"):
        clear_chat_history()
        st.rerun()
    
    # Display welcome message if chat is empty
    if not st.session_state.chat_history:
        st.info(get_welcome_message(lang_code))
    
    # Display chat history at the top
    st.markdown("### 💬 Sohbet")
    
    chat_container = st.container()
    with chat_container:
        for message in st.session_state.chat_history:
            display_chat_message(message['role'], message['content'])
    
    st.markdown("---")
    
    # Chat input below chat history
    st.markdown("### ✍️ Mesajınız")
    
    col1, col2 = st.columns([5, 1])
    
    with col1:
        user_input = st.text_input(
            "Mesajınızı yazın...",
            placeholder="Örn: Vejetaryen pizza önerir misiniz?",
            key="chat_input",
            label_visibility="collapsed"
        )
    
    with col2:
        send_button = st.button("📤 Gönder", type="primary", use_container_width=True)
    
    # Processing indicator - shown when message is being processed
    processing_placeholder = st.empty()
    
    # Show suggestions below chat input
    selected_suggestion = show_suggestions()
    
    # Process message
    if send_button or selected_suggestion:
        message = selected_suggestion if selected_suggestion else user_input
        
        if message:
            # Show processing indicator
            with processing_placeholder:
                st.info("🤖 Düşünüyorum...")
            
            # Add user message to chat
            add_chat_message('user', message)
            
            # Build filters based on preferences
            filters = {}
            if prefer_vegetarian:
                filters['vegetarian'] = True
            if prefer_vegan:
                filters['vegan'] = True
            if budget < 150:
                filters['max_price'] = budget
            if exclude_allergens:
                filters['exclude_allergens'] = exclude_allergens
            
            # Get AI response
            try:
                response = assistant.get_response(message, lang_code, filters)
                add_chat_message('assistant', response)
                
                # Clear processing indicator
                processing_placeholder.empty()
                
                # Try to extract menu items and show quick add buttons
                db = get_db()
                mentioned_items = extract_menu_items_from_response(response, db)
                
                if mentioned_items:
                    st.markdown("### 🍽️ Bahsedilen Ürünler")
                    cols = st.columns(min(len(mentioned_items), 3))
                    
                    for idx, item in enumerate(mentioned_items[:3]):  # Show max 3
                        with cols[idx]:
                            st.markdown(f"**{item.name}**")
                            st.caption(f"{item.price} ₺")
                            if st.button(f"➕ Sepete Ekle", key=f"quick_add_{item.id}"):
                                add_to_cart(item.id, item.name, item.price)
                                st.success(f"✅ {item.name} sepete eklendi!")
                
                db.close()
                
            except Exception as e:
                # Clear processing indicator on error
                processing_placeholder.empty()
                error_msg = f"Üzgünüm, bir hata oluştu: {str(e)}"
                add_chat_message('assistant', error_msg)
                st.error(error_msg)
            
            st.rerun()
    
    # Quick actions
    st.markdown("---")
    st.markdown("### 🎯 Hızlı İşlemler")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        if st.button("📖 Menüye Git", use_container_width=True):
            st.switch_page("pages/1_🍽️_Menu.py")
    
    with col2:
        if st.button("🛒 Sepet", use_container_width=True):
            st.switch_page("pages/2_🛒_Cart.py")
    
    with col3:
        if st.button("🏠 Ana Sayfa", use_container_width=True):
            st.switch_page("app.py")
    
    with col4:
        if st.button("❓ Yardım", use_container_width=True):
            st.info("""
            **AI Asistan Nasıl Kullanılır?**
            
            1. Sorunuzu doğal dille yazın
            2. Tercihlerinizi sidebar'dan ayarlayın
            3. Önerilen ürünleri direkt sepete ekleyin
            4. İstediğiniz kadar soru sorabilirsiniz
            
            **İpuçları:**
            - Spesifik olun: "acı pizza" vs "yemek"
            - Bütçenizi belirtin: "50 TL altında"
            - Alerjilerinizi bildirin
            - Vejetaryen/vegan tercihlerinizi seçin
            """)
    
    # Footer info
    st.markdown("---")
    st.caption("💡 AI asistan, Ollama ve LangChain kullanarak çalışır. Yanıtlar gerçek zamanlı üretilir.")

if __name__ == "__main__":
    main()
