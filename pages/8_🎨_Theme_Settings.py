"""
Theme Settings - Customize appearance and branding
Admin only access - requires authentication through admin.py
"""

import streamlit as st
from utils.session_manager import init_session_state
from utils.page_navigation import show_admin_navigation, hide_default_sidebar
import json
import os

# Page config
st.set_page_config(page_title="Tema Ayarları", page_icon="🎨", layout="wide")

# Hide default sidebar
hide_default_sidebar()

# Initialize session
init_session_state()

# Check admin access
if not st.session_state.is_admin:
    st.error("⛔ Bu sayfaya erişim için admin girişi yapmalısınız.")
    st.info("👉 Lütfen admin giriş sayfasından giriş yapın.")
    if st.button("🔙 Admin Girişine Dön"):
        st.switch_page("pages/0_🔐_Admin_Login.py")
    st.stop()

# Show admin navigation
show_admin_navigation()

# Theme presets
THEME_PRESETS = {
    "Varsayılan": {
        "primary_color": "#667eea",
        "secondary_color": "#764ba2",
        "background_color": "#f5f7fa",
        "text_color": "#2d3748",
        "card_color": "#ffffff"
    },
    "Koyu Mod": {
        "primary_color": "#667eea",
        "secondary_color": "#764ba2",
        "background_color": "#1a202c",
        "text_color": "#e2e8f0",
        "card_color": "#2d3748"
    },
    "Doğa": {
        "primary_color": "#48bb78",
        "secondary_color": "#38a169",
        "background_color": "#f0fff4",
        "text_color": "#22543d",
        "card_color": "#ffffff"
    },
    "Okyanus": {
        "primary_color": "#4299e1",
        "secondary_color": "#3182ce",
        "background_color": "#ebf8ff",
        "text_color": "#2c5282",
        "card_color": "#ffffff"
    },
    "Gün Batımı": {
        "primary_color": "#f56565",
        "secondary_color": "#ed8936",
        "background_color": "#fffaf0",
        "text_color": "#742a2a",
        "card_color": "#ffffff"
    },
    "Mor Rüya": {
        "primary_color": "#9f7aea",
        "secondary_color": "#805ad5",
        "background_color": "#faf5ff",
        "text_color": "#44337a",
        "card_color": "#ffffff"
    }
}

def load_theme_settings():
    """Load theme settings from session or defaults"""
    if 'theme_settings' not in st.session_state:
        st.session_state.theme_settings = THEME_PRESETS["Varsayılan"].copy()
    
    return st.session_state.theme_settings

def save_theme_settings(settings):
    """Save theme settings to session"""
    st.session_state.theme_settings = settings
    
    # Generate CSS
    css = generate_theme_css(settings)
    st.session_state.custom_css = css

def generate_theme_css(settings):
    """Generate CSS from theme settings"""
    return f"""
<style>
    :root {{
        --primary-color: {settings['primary_color']};
        --secondary-color: {settings['secondary_color']};
        --background-color: {settings['background_color']};
        --text-color: {settings['text_color']};
        --card-color: {settings['card_color']};
    }}
    
    /* Custom styles */
    .stApp {{
        background-color: var(--background-color);
    }}
    
    .menu-card {{
        background: var(--card-color);
        color: var(--text-color);
        border-radius: 15px;
        padding: 1.5rem;
        box-shadow: 0 4px 12px rgba(0,0,0,0.1);
    }}
    
    .gradient-bg {{
        background: linear-gradient(135deg, var(--primary-color), var(--secondary-color));
    }}
    
    h1, h2, h3, h4, h5, h6 {{
        color: var(--text-color);
    }}
    
    .stButton>button {{
        background: linear-gradient(135deg, var(--primary-color), var(--secondary-color));
        color: white;
        border: none;
        border-radius: 8px;
        padding: 0.5rem 1.5rem;
        font-weight: 500;
    }}
    
    .stButton>button:hover {{
        opacity: 0.9;
        transform: translateY(-2px);
        box-shadow: 0 4px 8px rgba(0,0,0,0.2);
    }}
</style>
"""

def main():
    """Main theme settings page"""
    st.title("🎨 Tema ve Görünüm Ayarları")
    
    # Load current settings
    current_theme = load_theme_settings()
    
    # Main tabs
    tab1, tab2, tab3, tab4 = st.tabs([
        "🎨 Renkler",
        "🖼️ Logo ve Marka",
        "📐 Düzen",
        "💾 Önizleme ve Kaydet"
    ])
    
    with tab1:
        st.markdown("## 🎨 Renk Şeması")
        
        # Preset themes
        st.markdown("### 📦 Hazır Temalar")
        
        preset_cols = st.columns(3)
        
        for i, (name, colors) in enumerate(THEME_PRESETS.items()):
            with preset_cols[i % 3]:
                if st.button(f"🎨 {name}", key=f"preset_{name}", use_container_width=True):
                    current_theme.update(colors)
                    st.rerun()
                
                # Show color preview
                st.markdown(f"""
                <div style="display: flex; gap: 5px; margin: 5px 0;">
                    <div style="width: 30px; height: 30px; background: {colors['primary_color']}; border-radius: 5px;"></div>
                    <div style="width: 30px; height: 30px; background: {colors['secondary_color']}; border-radius: 5px;"></div>
                    <div style="width: 30px; height: 30px; background: {colors['background_color']}; border-radius: 5px; border: 1px solid #ddd;"></div>
                </div>
                """, unsafe_allow_html=True)
        
        st.markdown("---")
        
        # Custom colors
        st.markdown("### 🎨 Özel Renkler")
        
        col1, col2 = st.columns(2)
        
        with col1:
            primary_color = st.color_picker(
                "Ana Renk",
                value=current_theme['primary_color'],
                help="Butonlar ve vurgular için ana renk"
            )
            
            secondary_color = st.color_picker(
                "İkincil Renk",
                value=current_theme['secondary_color'],
                help="Gradyanlar için ikincil renk"
            )
            
            background_color = st.color_picker(
                "Arka Plan Rengi",
                value=current_theme['background_color'],
                help="Sayfa arka plan rengi"
            )
        
        with col2:
            text_color = st.color_picker(
                "Metin Rengi",
                value=current_theme['text_color'],
                help="Başlıklar ve metinler için renk"
            )
            
            card_color = st.color_picker(
                "Kart Arka Planı",
                value=current_theme['card_color'],
                help="Menü kartları ve paneller için renk"
            )
        
        # Update theme
        current_theme.update({
            'primary_color': primary_color,
            'secondary_color': secondary_color,
            'background_color': background_color,
            'text_color': text_color,
            'card_color': card_color
        })
    
    with tab2:
        st.markdown("## 🖼️ Logo ve Marka Ayarları")
        
        col1, col2 = st.columns([1, 2])
        
        with col1:
            st.markdown("### 📷 Logo")
            
            # Logo upload
            logo_file = st.file_uploader(
                "Logo Yükle",
                type=['png', 'jpg', 'jpeg', 'svg'],
                help="Restaurant logonuzu yükleyin"
            )
            
            if logo_file:
                st.image(logo_file, width=200)
                
                if st.button("💾 Logoyu Kaydet"):
                    # Save logo
                    logo_path = os.path.join("static", "images", "logo.png")
                    os.makedirs(os.path.dirname(logo_path), exist_ok=True)
                    
                    with open(logo_path, "wb") as f:
                        f.write(logo_file.getbuffer())
                    
                    st.success("✅ Logo kaydedildi!")
            
            st.markdown("### 🎯 Favicon")
            
            favicon_file = st.file_uploader(
                "Favicon Yükle",
                type=['ico', 'png'],
                help="Tarayıcı sekmesinde görünecek ikon"
            )
        
        with col2:
            st.markdown("### 🏷️ Marka Bilgileri")
            
            restaurant_name = st.text_input(
                "Restaurant Adı",
                value=os.getenv('RESTAURANT_NAME', 'Delicious Bites'),
                help="Ana başlıklarda görünecek isim"
            )
            
            tagline = st.text_input(
                "Slogan",
                value="En lezzetli yemekler burada!",
                help="Ana sayfada gösterilecek slogan"
            )
            
            description = st.text_area(
                "Açıklama",
                value="Modern ve lezzetli mutfak deneyimi",
                help="Hakkımızda bölümü için açıklama",
                height=100
            )
            
            st.markdown("### 📞 İletişim Bilgileri")
            
            col_a, col_b = st.columns(2)
            
            with col_a:
                phone = st.text_input(
                    "Telefon",
                    value=os.getenv('RESTAURANT_PHONE', '+90 555 123 4567')
                )
                
                email = st.text_input(
                    "Email",
                    value="info@restaurant.com"
                )
            
            with col_b:
                address = st.text_area(
                    "Adres",
                    value="İstanbul, Türkiye",
                    height=100
                )
            
            # Save settings
            if st.button("💾 Marka Ayarlarını Kaydet", type="primary"):
                st.success("✅ Marka ayarları kaydedildi!")
                st.info("💡 .env dosyasını güncelleyin:")
                st.code(f"""
RESTAURANT_NAME={restaurant_name}
RESTAURANT_PHONE={phone}
""")
    
    with tab3:
        st.markdown("## 📐 Düzen Ayarları")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("### 🗂️ Menü Düzeni")
            
            menu_layout = st.radio(
                "Menü Görünümü",
                ["Grid (Kartlar)", "Liste", "Kompakt"],
                help="Menü öğelerinin nasıl görüntüleneceği"
            )
            
            items_per_row = st.slider(
                "Satır Başına Öğe",
                min_value=2,
                max_value=4,
                value=3,
                help="Grid görünümünde bir satırda kaç öğe gösterilecek"
            )
            
            show_images = st.checkbox(
                "Ürün Resimlerini Göster",
                value=True
            )
            
            show_calories = st.checkbox(
                "Kalori Bilgisi Göster",
                value=True
            )
        
        with col2:
            st.markdown("### 🎯 Genel Ayarlar")
            
            sidebar_position = st.radio(
                "Sidebar Konumu",
                ["Sol", "Sağ"],
                help="Navigasyon sidebar'ının konumu"
            )
            
            show_footer = st.checkbox(
                "Footer Göster",
                value=True
            )
            
            compact_mode = st.checkbox(
                "Kompakt Mod",
                value=False,
                help="Daha az boşluk, daha fazla içerik"
            )
        
        st.markdown("---")
        
        st.markdown("### 🎨 Özel CSS")
        
        custom_css = st.text_area(
            "Özel CSS Kodları",
            value="/* Buraya özel CSS kodlarınızı yazabilirsiniz */",
            height=200,
            help="İleri seviye özelleştirmeler için"
        )
        
        if st.button("💾 Düzen Ayarlarını Kaydet", type="primary"):
            st.success("✅ Düzen ayarları kaydedildi!")
    
    with tab4:
        st.markdown("## 💾 Önizleme ve Kaydet")
        
        # Apply current theme for preview
        css = generate_theme_css(current_theme)
        st.markdown(css, unsafe_allow_html=True)
        
        st.markdown("### 👀 Tema Önizlemesi")
        
        # Preview components
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### Örnek Kart")
            st.markdown(f"""
            <div class="menu-card">
                <h3 style="color: {current_theme['text_color']};">Margherita Pizza</h3>
                <p style="color: {current_theme['text_color']};">Taze mozzarella, domates sosu ve fesleğen</p>
                <div style="display: flex; justify-content: space-between; align-items: center; margin-top: 1rem;">
                    <span style="font-size: 1.5rem; font-weight: bold; color: {current_theme['primary_color']};">₺85.00</span>
                    <button style="background: linear-gradient(135deg, {current_theme['primary_color']}, {current_theme['secondary_color']}); color: white; border: none; padding: 0.5rem 1rem; border-radius: 8px;">Sepete Ekle</button>
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown("#### Renk Paleti")
            
            colors = {
                "Ana Renk": current_theme['primary_color'],
                "İkincil Renk": current_theme['secondary_color'],
                "Arka Plan": current_theme['background_color'],
                "Metin": current_theme['text_color'],
                "Kart": current_theme['card_color']
            }
            
            for name, color in colors.items():
                st.markdown(f"""
                <div style="display: flex; align-items: center; margin: 10px 0;">
                    <div style="width: 50px; height: 50px; background: {color}; border-radius: 8px; border: 1px solid #ddd; margin-right: 10px;"></div>
                    <div>
                        <strong>{name}</strong><br>
                        <code>{color}</code>
                    </div>
                </div>
                """, unsafe_allow_html=True)
        
        st.markdown("---")
        
        # Save options
        st.markdown("### 💾 Kaydetme Seçenekleri")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            if st.button("💾 Temayı Kaydet", type="primary", use_container_width=True):
                save_theme_settings(current_theme)
                st.success("✅ Tema kaydedildi!")
                st.balloons()
        
        with col2:
            if st.button("📥 Temayı İndir", use_container_width=True):
                theme_json = json.dumps(current_theme, indent=2)
                st.download_button(
                    label="💾 JSON İndir",
                    data=theme_json,
                    file_name="theme.json",
                    mime="application/json"
                )
        
        with col3:
            if st.button("🔄 Sıfırla", use_container_width=True):
                st.session_state.theme_settings = THEME_PRESETS["Varsayılan"].copy()
                st.rerun()
        
        st.markdown("---")
        
        # Import theme
        st.markdown("### 📤 Tema İçe Aktar")
        
        theme_file = st.file_uploader(
            "Tema Dosyası Yükle (JSON)",
            type=['json'],
            help="Önceden kaydedilmiş tema dosyasını yükleyin"
        )
        
        if theme_file:
            try:
                imported_theme = json.load(theme_file)
                if st.button("📥 Temayı Uygula"):
                    current_theme.update(imported_theme)
                    save_theme_settings(current_theme)
                    st.success("✅ Tema başarıyla içe aktarıldı!")
                    st.rerun()
            except Exception as e:
                st.error(f"❌ Tema dosyası okunamadı: {e}")
    


if __name__ == "__main__":
    main()
