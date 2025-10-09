"""
Page Navigation Utilities - Dynamic sidebar menu based on user role
"""

import streamlit as st
from streamlit_option_menu import option_menu

def show_customer_navigation():
    """Show customer navigation menu"""
    # Get restaurant info for logo
    from database.db_manager import get_db
    db = get_db()
    restaurant = db.get_restaurant_info()
    db.close()
    
    with st.sidebar:
        # Show logo at the top of sidebar (responsive, smaller on mobile)
        if restaurant.logo_url:
            try:
                # Use responsive columns for mobile
                col1, col2, col3 = st.columns([1, 1.5, 1])
                with col2:
                    st.image(restaurant.logo_url, use_container_width=True)
            except:
                pass
        
        # Show table number if assigned (dark mode compatible)
        if st.session_state.get('table_number'):
            st.markdown(f"""
            <div style='
                text-align: center; 
                padding: 0.3rem; 
                background-color: #e3f2fd; 
                color: #000000;
                border-radius: 8px; 
                margin: 0.5rem 0;
            '>
                <strong>📍 Masa: {st.session_state.table_number}</strong>
            </div>
            """, unsafe_allow_html=True)
        
        # Navigation menu
        st.markdown("##### 📱 Menü")
    
    customer_pages = {
        "🏠 Ana Sayfa": "app.py",
        "🍽️ Menü": "pages/1_🍽️_Menu.py",
        "🛒 Sepet": "pages/2_🛒_Cart.py",
        "💬 AI Asistan": "pages/3_💬_AI_Assistant.py",
    }
    
    with st.sidebar:
        for name, page in customer_pages.items():
            if st.button(name, use_container_width=True):
                st.switch_page(page)
        
        # Additional CSS for responsive logo sizing
        st.markdown("""
        <style>
            /* Mobile responsive logo */
            @media (max-width: 768px) {
                [data-testid="stSidebar"] img {
                    max-width: 80px !important;
                    margin: 0 auto;
                }
            }
        </style>
        """, unsafe_allow_html=True)

def show_admin_navigation():
    """Show admin navigation menu"""
    admin_pages = {
        "📊 Dashboard": "pages/4_📊_Admin_Dashboard.py",
        "🏢 Markalar": "pages/11_🏢_Brand_Management.py",
        "🏓 Masa Yönetimi": "pages/5_🏓_Table_Management.py",
        "🍽️ Menü Yönetimi": "pages/10_🍽️_Menu_Management.py",
        "📈 Raporlar": "pages/6_📈_Reports.py",
        "🔔 Bildirimler": "pages/7_🔔_Notifications.py",
        "🎨 Tema": "pages/8_🎨_Theme_Settings.py",
        "📂 Kategoriler": "pages/9_📂_Category_Management.py",
        
    }
    
    with st.sidebar:
        st.markdown("---")
        st.markdown("### 👨‍💼 Admin Paneli")
        for name, page in admin_pages.items():
            if st.button(name, use_container_width=True):
                st.switch_page(page)
        
        # Logout button
        st.markdown("---")
        if st.button("🚪 Çıkış Yap", use_container_width=True, type="secondary"):
            from utils.session_manager import toggle_admin_mode
            toggle_admin_mode()
            st.switch_page("pages/0_🔐_Admin_Login.py")

def hide_default_sidebar():
    """Hide default Streamlit sidebar navigation - must be called immediately after set_page_config"""
    # Inject CSS + JavaScript for immediate hiding to prevent flickering
    st.markdown("""
    <style>
        /* CRITICAL: Hide default Streamlit sidebar navigation immediately */
        [data-testid="stSidebarNav"] {
            display: none !important;
            visibility: hidden !important;
            height: 0 !important;
            max-height: 0 !important;
            overflow: hidden !important;
            position: absolute !important;
            pointer-events: none !important;
            opacity: 0 !important;
        }
        
        /* Additional robust selectors */
        section[data-testid="stSidebarNav"],
        div[data-testid="stSidebarNav"],
        .css-1544g2n,
        [data-testid="stSidebarNav"] ul,
        [data-testid="stSidebarNav"] li,
        nav[aria-label="Page navigation"] {
            display: none !important;
            visibility: hidden !important;
            opacity: 0 !important;
        }
        
        /* Prevent any transition/animation that causes flickering */
        [data-testid="stSidebarNav"] * {
            transition: none !important;
            animation: none !important;
        }
    </style>
    
    <script>
        // Immediately hide sidebar nav when DOM loads (before CSS)
        (function() {
            const hideNav = function() {
                const navElements = document.querySelectorAll('[data-testid="stSidebarNav"]');
                navElements.forEach(el => {
                    el.style.display = 'none';
                    el.style.visibility = 'hidden';
                    el.style.opacity = '0';
                });
            };
            
            // Run immediately
            hideNav();
            
            // Run on DOM ready
            if (document.readyState === 'loading') {
                document.addEventListener('DOMContentLoaded', hideNav);
            }
            
            // Run on load as fallback
            window.addEventListener('load', hideNav);
            
            // Use MutationObserver to catch dynamic additions
            const observer = new MutationObserver(hideNav);
            observer.observe(document.body, { childList: true, subtree: true });
        })();
    </script>
    """, unsafe_allow_html=True)
