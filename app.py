"""
QR Menu AI - Main Streamlit Application
"""

import streamlit as st
from streamlit_option_menu import option_menu
import os
from dotenv import load_dotenv
from utils.session_manager import init_session_state, get_cart_count
from utils.page_navigation import show_customer_navigation, hide_default_sidebar
from database.db_manager import get_db

# Load environment variables
load_dotenv()

# Get restaurant info for dynamic branding
db = get_db()
restaurant = db.get_restaurant_info()
db.close()

# Page config with dynamic title
st.set_page_config(
    page_title=f"{restaurant.name_tr} - AI Menu",
    page_icon=restaurant.icon_url if restaurant.icon_url else "🍕",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Hide default Streamlit sidebar navigation
hide_default_sidebar()

# Custom CSS
st.markdown("""
<style>
    .main-header {
        text-align: center;
        padding: 1rem;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border-radius: 10px;
        margin-bottom: 2rem;
    }
    .cart-badge {
        background-color: #ff4b4b;
        color: white;
        border-radius: 50%;
        padding: 0.2rem 0.5rem;
        font-size: 0.8rem;
        font-weight: bold;
    }
    .menu-card {
        border: 1px solid #ddd;
        border-radius: 10px;
        padding: 1rem;
        margin: 0.5rem 0;
        transition: transform 0.2s;
    }
    .menu-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 4px 8px rgba(0,0,0,0.1);
    }
</style>
""", unsafe_allow_html=True)

# Initialize session
init_session_state()

def show_header():
    """Display app header with dynamic restaurant info"""
    db = get_db()
    restaurant = db.get_restaurant_info()
    db.close()
    
    # # Show logo if available
    # if restaurant.logo_url:
    #     col1, col2, col3 = st.columns([1, 2, 1])
    #     with col2:
    #         try:
    #             st.image(restaurant.logo_url, width=200)
    #         except:
    #             pass
    
    # st.markdown(f"""
    # <div class="main-header">
    #     <h1>{restaurant.name_tr}</h1>
    #     <p>AI Güçlü Dijital Menü Sistemi</p>
    # </div>
    # """, unsafe_allow_html=True)

def check_table_assignment():
    """Check if user has been assigned a table"""
    # Get table number from URL parameters
    query_params = st.query_params
    
    if 'table' in query_params and not st.session_state.table_number:
        try:
            table_num = int(query_params['table'])
            db = get_db()
            table = db.get_table_by_number(table_num)
            
            if table:
                from utils.session_manager import set_table_number
                set_table_number(table_num, table.id)
                st.success(f"✅ Masa {table_num}'e hoş geldiniz!")
            else:
                st.error(f"⚠️ Masa {table_num} bulunamadı!")
            
            db.close()
        except ValueError:
            st.error("⚠️ Geçersiz masa numarası!")
    
    # Manual table selection for testing
    if not st.session_state.table_number:
        st.warning("⚠️ Lütfen QR kodu tarayın veya masa numaranızı girin.")
        
        col1, col2 = st.columns([3, 1])
        with col1:
            table_input = st.number_input(
                "Masa Numarası",
                min_value=1,
                max_value=20,
                value=1,
                help="Test için masa numarası girin"
            )
        with col2:
            st.write("")  # Spacing
            st.write("")  # Spacing
            if st.button("Onayla", type="primary"):
                db = get_db()
                table = db.get_table_by_number(table_input)
                if table:
                    from utils.session_manager import set_table_number
                    set_table_number(table_input, table.id)
                    st.rerun()
                else:
                    st.error("Masa bulunamadı!")
                db.close()
        
        st.stop()

def show_sidebar():
    """Display custom sidebar navigation"""
    # Show customer navigation menu (includes logo and table number)
    show_customer_navigation()

def show_home():
    """Display home page"""
    st.markdown("## 👋 Hoş Geldiniz!")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        ### 📖 Menü
        - Tüm yemekleri görün
        - Kategorilere göre filtreleyin
        - Fiyat ve detayları öğrenin
        """)
        if st.button("Menüye Git", key="goto_menu", type="primary"):
            st.switch_page("pages/1_🍽️_Menu.py")
    
    with col2:
        st.markdown("""
        ### 🤖 AI Asistan
        - Sorularınızı sorun
        - Öneri alın
        - Alerjen kontrolü yapın
        """)
        if st.button("AI ile Konuş", key="goto_ai", type="primary"):
            st.switch_page("pages/3_💬_AI_Assistant.py")
    
    with col3:
        st.markdown("""
        ### 🛒 Sipariş
        - Sepetinizi görün
        - Sipariş verin
        - Durumunu takip edin
        """)
        cart_count = get_cart_count()
        if cart_count > 0:
            st.info(f"Sepetinizde {cart_count} ürün var")
            if st.button("Sepete Git", key="goto_cart", type="primary"):
                st.switch_page("pages/2_🛒_Cart.py")
    
    # Popular items
    st.markdown("---")
    st.markdown("## ⭐ Popüler Ürünler")
    
    db = get_db()
    popular = db.get_popular_items(limit=6)
    
    cols = st.columns(3)
    for i, item in enumerate(popular):
        with cols[i % 3]:
            st.markdown(f"""
            <div class="menu-card">
                <h4>{item.name}</h4>
                <p>{item.description[:50]}...</p>
                <p><strong>{item.price} TL</strong></p>
            </div>
            """, unsafe_allow_html=True)
            
            if st.button(f"Sepete Ekle", key=f"add_pop_{item.id}"):
                from utils.session_manager import add_to_cart
                add_to_cart(item.id, item.name, item.price)
                st.success(f"✅ {item.name} sepete eklendi!")
                st.rerun()
    
    db.close()
    
    # Restaurant info
    st.markdown("---")
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        ### 📍 İletişim
        - 📞 Telefon: +90 555 123 4567
        - 📧 Email: info@lapizzabella.com
        - 🏠 Adres: Merkez Mah. Lezzet Sok. No:10
        """)
    
    with col2:
        st.markdown("""
        ### ⏰ Çalışma Saatleri
        - Pazartesi - Cuma: 11:00 - 23:00
        - Cumartesi - Pazar: 10:00 - 00:00
        """)

def main():
    """Main application"""
    show_header()
    
    # Check table assignment
    check_table_assignment()
    
    # Show sidebar navigation
    show_sidebar()
    
    # Show home page content
    show_home()

if __name__ == "__main__":
    main()
