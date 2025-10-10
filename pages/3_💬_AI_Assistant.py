"""
AI Assistant Page - Chat with AI menu assistant
"""

import streamlit as st
from ai.assistant import get_assistant
from ai.prompts import get_welcome_message
from utils.session_manager import init_session_state, add_chat_message, clear_chat_history, add_to_cart, get_session_id, clear_cart
from utils.page_navigation import show_customer_navigation, hide_default_sidebar
from database.db_manager import get_db
from utils.ai_helper import (
    parse_ai_response_for_products,
    create_product_card,
    create_order_confirmation_message
)

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

def create_order_from_cart():
    """Create order from cart items"""
    if not st.session_state.cart:
        return None, "Sepetiniz boş!"
    
    if not st.session_state.table_number:
        return None, "Masa numarası bulunamadı!"
    
    try:
        db = get_db()
        
        # Create order
        order = db.create_order(
            table_id=st.session_state.table_id,
            session_id=get_session_id()
        )
        
        # Add items to order
        for cart_item in st.session_state.cart:
            db.add_order_item(
                order_id=order.id,
                menu_item_id=cart_item['item_id'],
                quantity=cart_item['quantity'],
                notes=cart_item.get('notes', '')
            )
        
        # Update table status
        db.update_table_status(
            table_id=st.session_state.table_id,
            status='occupied',
            session_id=get_session_id()
        )
        
        # Save order ID
        st.session_state.current_order_id = order.id
        
        # Send notification if enabled
        try:
            from utils.notification_manager import get_notification_manager
            nm = get_notification_manager()
            items = [
                {
                    'name': item['item_name'],
                    'quantity': item['quantity']
                }
                for item in st.session_state.cart
            ]
            nm.notify_new_order(
                order_id=order.id,
                table_number=st.session_state.table_number,
                total_amount=st.session_state.cart_total,
                items=items
            )
        except Exception as e:
            print(f"Notification error: {e}")
        
        db.close()
        
        # Clear cart
        clear_cart()
        
        return order.id, None
        
    except Exception as e:
        return None, f"Sipariş oluşturulamadı: {str(e)}"

def display_chat_message(role, content):
    """Display a chat message"""
    if role == "user":
        with st.chat_message("user"):
            st.markdown(f"**👤 Siz:**\n\n{content}")
    else:
        # Parse AI response for product IDs
        clean_content = content
        if "[PRODUCT:" in content:
            # Extract products and clean text
            product_ids, clean_text = parse_ai_response_for_products(content)
            clean_content = clean_text
            
        with st.chat_message("assistant"):
            st.markdown(f"**🤖 AI Asistan:**\n\n{clean_content}")

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
            
            # If it's an assistant message with product IDs, show product cards
            if message['role'] == 'assistant' and '[PRODUCT:' in message['content']:
                product_ids, _ = parse_ai_response_for_products(message['content'])
                
                if product_ids:
                    db = get_db()
                    st.markdown("#### 🍽️ Önerilen Ürünler")
                    
                    # Create unique suffix from timestamp
                    timestamp_str = str(message.get('timestamp', '')).replace(' ', '_').replace(':', '_').replace('.', '_')
                    
                    # Display up to 3 products per row
                    cols_per_row = min(len(product_ids), 3)
                    for i in range(0, len(product_ids), cols_per_row):
                        cols = st.columns(cols_per_row)
                        for j, product_id in enumerate(product_ids[i:i+cols_per_row]):
                            product = db.get_menu_item(product_id)
                            if product:
                                with cols[j]:
                                    create_product_card(product, f"{timestamp_str}_{product_id}")
                    
                    db.close()
    
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
            # Set AI processing flag - DISABLE BUTTONS
            st.session_state.ai_is_processing = True
            
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
                # Check if waiting for order confirmation
                if st.session_state.get('waiting_order_confirmation', False):
                    confirmation_yes = ['evet', 'yes', 'tamam', 'okay', 'ok', 'onaylıyorum', 'onay']
                    confirmation_no = ['hayır', 'no', 'vazgeç', 'iptal', 'cancel']
                    
                    if any(keyword in message.lower() for keyword in confirmation_yes):
                        # User confirmed the order - Create actual order in database
                        st.session_state.waiting_order_confirmation = False
                        
                        # Create order
                        order_id, error = create_order_from_cart()
                        
                        if order_id:
                            success_msg = f"""
✅ **Siparişiniz Alındı!**

📝 Sipariş No: #{order_id}
Siparişiniz mutfağa iletildi. Yakında hazırlanmaya başlanacak.
Afiyet olsun! 🍽️✨
""" if lang_code == 'tr' else f"""
✅ **Order Confirmed!**

📝 Order No: #{order_id}
Your order has been sent to the kitchen. It will be prepared shortly.
Enjoy your meal! 🍽️✨
"""
                        else:
                            success_msg = f"""
❌ **Sipariş Hatası**

{error}
Lütfen tekrar deneyin veya garsondan yardım isteyin.
""" if lang_code == 'tr' else f"""
❌ **Order Error**

{error}
Please try again or ask a waiter for help.
"""
                        
                        add_chat_message('assistant', success_msg)
                        
                        # Clear processing indicator and re-enable buttons
                        processing_placeholder.empty()
                        st.session_state.ai_is_processing = False
                        
                        st.rerun()
                        
                    elif any(keyword in message.lower() for keyword in confirmation_no):
                        # User cancelled the order
                        st.session_state.waiting_order_confirmation = False
                        
                        cancel_msg = """
Sipariş iptal edildi. Başka bir şey sipariş etmek ister misiniz?
""" if lang_code == 'tr' else """
Order cancelled. Would you like to order something else?
"""
                        add_chat_message('assistant', cancel_msg)
                        
                        # Clear processing indicator and re-enable buttons
                        processing_placeholder.empty()
                        st.session_state.ai_is_processing = False
                        
                        st.rerun()
                    else:
                        # User said something else, remind them to confirm
                        reminder_msg = """
Lütfen siparişinizi onaylamak için 'evet' veya iptal etmek için 'hayır' yazın.
""" if lang_code == 'tr' else """
Please type 'yes' to confirm your order or 'no' to cancel.
"""
                        add_chat_message('assistant', reminder_msg)
                        
                        # Clear processing indicator and re-enable buttons
                        processing_placeholder.empty()
                        st.session_state.ai_is_processing = False
                        
                        st.rerun()
                    
                    # Don't process further if waiting for confirmation
                    return
                
                response = assistant.get_response(message, lang_code, filters)
                
                # Check if user is asking to confirm order
                confirm_keywords = ['sipariş ver', 'sipariş et', 'onayla', 'confirm order', 'place order', 'checkout']
                if any(keyword in message.lower() for keyword in confirm_keywords):
                    # Show order confirmation
                    if st.session_state.cart:
                        order_msg = create_order_confirmation_message(
                            st.session_state.cart,
                            st.session_state.cart_total,
                            lang_code
                        )
                        add_chat_message('assistant', order_msg)
                        
                        # Set flag to wait for confirmation
                        st.session_state.waiting_order_confirmation = True
                        
                        # Clear processing indicator and re-enable buttons
                        processing_placeholder.empty()
                        st.session_state.ai_is_processing = False
                        
                        st.rerun()
                    else:
                        add_chat_message('assistant', 
                            "Sepetiniz boş görünüyor. Önce sepete ürün eklemelisiniz." if lang_code == 'tr' 
                            else "Your cart appears to be empty. Please add items to your cart first.")
                        
                        # Clear processing indicator and re-enable buttons
                        processing_placeholder.empty()
                        st.session_state.ai_is_processing = False
                        
                        st.rerun()
                else:
                    # Regular AI response
                    add_chat_message('assistant', response)
                    
                    # Clear processing indicator and re-enable buttons
                    processing_placeholder.empty()
                    st.session_state.ai_is_processing = False
                    
                    st.rerun()
                
            except Exception as e:
                # Clear processing indicator and re-enable buttons on error
                processing_placeholder.empty()
                st.session_state.ai_is_processing = False
                
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
