"""
Admin Login Page - Authentication for admin panel
"""

import streamlit as st
from utils.session_manager import init_session_state, toggle_admin_mode
from utils.page_navigation import hide_default_sidebar
import os

# Page config
st.set_page_config(page_title="Admin Girişi", page_icon="🔐", layout="centered")

# Hide default sidebar navigation
hide_default_sidebar()

# Initialize session
init_session_state()

# Custom CSS
st.markdown("""
<style>
    .login-container {
        max-width: 400px;
        margin: 0 auto;
        padding: 2rem;
    }
    .login-header {
        text-align: center;
        margin-bottom: 2rem;
    }
    .login-box {
        background: white;
        border-radius: 15px;
        padding: 2rem;
        box-shadow: 0 4px 12px rgba(0,0,0,0.1);
    }
    .restaurant-logo {
        text-align: center;
        font-size: 4rem;
        margin-bottom: 1rem;
    }
</style>
""", unsafe_allow_html=True)

def main():
    """Main admin login page"""
    
    # Check if already logged in - redirect to dashboard
    if st.session_state.get('is_admin', False):
        st.switch_page("pages/4_📊_Admin_Dashboard.py")
    
    # Login form
    st.markdown('<div class="login-container">', unsafe_allow_html=True)
    
    st.markdown('<div class="restaurant-logo">🍕</div>', unsafe_allow_html=True)
    
    st.markdown(f"""
    <div class="login-header">
        <h1>🔐 Admin Girişi</h1>
        <p>{os.getenv('RESTAURANT_NAME', 'QR Menu AI')}</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown('<div class="login-box">', unsafe_allow_html=True)
    
    with st.form("login_form"):
        username = st.text_input(
            "👤 Kullanıcı Adı",
            placeholder="admin",
            help="Varsayılan: admin"
        )
        
        password = st.text_input(
            "🔑 Şifre",
            type="password",
            placeholder="••••••••",
            help="Varsayılan: admin123"
        )
        
        remember_me = st.checkbox("Beni Hatırla")
        
        submitted = st.form_submit_button("🚀 Giriş Yap", type="primary", use_container_width=True)
        
        if submitted:
            # Simple authentication (in production, use proper auth)
            admin_username = os.getenv('ADMIN_USERNAME', 'admin')
            admin_password = os.getenv('ADMIN_PASSWORD', 'admin123')
            
            if username == admin_username and password == admin_password:
                toggle_admin_mode()
                if remember_me:
                    st.session_state.remember_admin = True
                st.success("✅ Giriş başarılı! Dashboard'a yönlendiriliyorsunuz...")
                st.balloons()
                # Redirect to dashboard
                st.switch_page("pages/4_📊_Admin_Dashboard.py")
            else:
                st.error("❌ Kullanıcı adı veya şifre hatalı!")
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Info box
    st.markdown("---")
    st.info("""
    💡 **Test Bilgileri**
    
    Kullanıcı Adı: `admin`  
    Şifre: `admin123`
    
    ⚠️ Production ortamında .env dosyasından değiştirin!
    """)
    
    # Back to home
    if st.button("⬅️ Ana Sayfaya Dön", use_container_width=True):
        st.switch_page("app.py")
    
    st.markdown('</div>', unsafe_allow_html=True)

if __name__ == "__main__":
    main()
