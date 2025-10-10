"""
Brand/Restaurant Management Page
Manage restaurant information, logo, icon, and social media
"""

import streamlit as st
from database.db_manager import get_db
import json
import os
from datetime import datetime
from utils.session_manager import init_session_state
from utils.page_navigation import show_admin_navigation, hide_default_sidebar

# Page config
st.set_page_config(
    page_title="Marka Yönetimi",
    page_icon="🏢",
    layout="wide"
)

# Initialize session
init_session_state()

# Check admin authentication
if not st.session_state.get('is_admin', False):
    st.error("🔒 Bu sayfaya erişim için admin girişi gereklidir!")
    st.stop()

# Database connection
db = get_db()

# Show admin navigation
show_admin_navigation()

# Page header
st.title("🏢 Marka Yönetimi")
st.markdown("---")

# Get current restaurant info
restaurant = db.get_restaurant_info()

# Parse JSON fields
try:
    working_hours = json.loads(restaurant.working_hours) if restaurant.working_hours else {}
except:
    working_hours = {}

try:
    social_media = json.loads(restaurant.social_media) if restaurant.social_media else {}
except:
    social_media = {}

# Create tabs
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "📋 Temel Bilgiler",
    "🎨 Görsel Kimlik",
    "📞 İletişim Bilgileri",
    "🌐 Sosyal Medya",
    "🤖 AI Asistan"
])

# ========================
# TAB 1: BASIC INFO
# ========================
with tab1:
    st.markdown("### 📋 Restoran Temel Bilgileri")
    
    with st.form("basic_info_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### 🇹🇷 Türkçe Bilgiler")
            name_tr = st.text_input(
                "Restoran Adı (TR)",
                value=restaurant.name_tr,
                help="Türkçe restoran ismi"
            )
            about_tr = st.text_area(
                "Hakkımızda (TR)",
                value=restaurant.about_tr or "",
                height=150,
                help="Restoranınız hakkında kısa açıklama"
            )
        
        with col2:
            st.markdown("#### 🇬🇧 English Information")
            name_en = st.text_input(
                "Restaurant Name (EN)",
                value=restaurant.name_en,
                help="English restaurant name"
            )
            about_en = st.text_area(
                "About Us (EN)",
                value=restaurant.about_en or "",
                height=150,
                help="Brief description about your restaurant"
            )
        
        st.markdown("---")
        st.markdown("#### ⏰ Çalışma Saatleri")
        
        col1, col2, col3 = st.columns(3)
        
        days = [
            ("Pazartesi", "Monday"),
            ("Salı", "Tuesday"),
            ("Çarşamba", "Wednesday"),
            ("Perşembe", "Thursday"),
            ("Cuma", "Friday"),
            ("Cumartesi", "Saturday"),
            ("Pazar", "Sunday")
        ]
        
        new_working_hours = {}
        for i, (day_tr, day_en) in enumerate(days):
            col = [col1, col2, col3][i % 3]
            with col:
                hours = st.text_input(
                    f"{day_tr}",
                    value=working_hours.get(day_tr, "10:00 - 23:00"),
                    key=f"hours_{day_tr}",
                    help="Örn: 10:00 - 23:00 veya Kapalı"
                )
                new_working_hours[day_tr] = hours
        
        submitted = st.form_submit_button("💾 Kaydet", type="primary", use_container_width=True)
        
        if submitted:
            try:
                db.update_restaurant_info(
                    name_tr=name_tr,
                    name_en=name_en,
                    about_tr=about_tr,
                    about_en=about_en,
                    working_hours=json.dumps(new_working_hours, ensure_ascii=False)
                )
                st.success("✅ Temel bilgiler başarıyla güncellendi!")
                st.balloons()
                st.rerun()
            except Exception as e:
                st.error(f"❌ Hata: {e}")

# ========================
# TAB 2: BRANDING
# ========================
with tab2:
    st.markdown("### 🎨 Görsel Kimlik")
    
    col1, col2 = st.columns(2)
    
    # LOGO
    with col1:
        st.markdown("#### 🖼️ Logo")
        
        if restaurant.logo_url:
            st.markdown("**Mevcut Logo:**")
            try:
                st.image(restaurant.logo_url, width=200)
                st.caption(f"📁 {restaurant.logo_url}")
            except:
                st.caption(f"📁 {restaurant.logo_url}")
        
        with st.form("logo_form"):
            logo_file = st.file_uploader(
                "Yeni Logo Yükle",
                type=['png', 'jpg', 'jpeg', 'svg', 'webp'],
                help="Önerilen boyut: 300x300 px veya daha büyük"
            )
            logo_url = st.text_input(
                "veya Logo URL",
                value="" if logo_file else (restaurant.logo_url or ""),
                help="Dış kaynaklı logo URL'si"
            )
            delete_logo = st.checkbox("🗑️ Logoyu Sil")
            
            submit_logo = st.form_submit_button("💾 Logo Güncelle", use_container_width=True)
            
            if submit_logo:
                try:
                    new_logo_url = None
                    
                    if delete_logo:
                        # Delete old logo file if exists
                        if restaurant.logo_url and restaurant.logo_url.startswith("static/"):
                            if os.path.exists(restaurant.logo_url):
                                os.remove(restaurant.logo_url)
                        new_logo_url = None
                    elif logo_file:
                        # Upload new logo
                        upload_dir = "static/images/brand"
                        os.makedirs(upload_dir, exist_ok=True)
                        
                        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                        file_extension = logo_file.name.split('.')[-1]
                        filename = f"logo_{timestamp}.{file_extension}"
                        filepath = os.path.join(upload_dir, filename)
                        
                        with open(filepath, 'wb') as f:
                            f.write(logo_file.getbuffer())
                        
                        new_logo_url = filepath
                        st.success(f"📸 Logo yüklendi: {filename}")
                    elif logo_url:
                        new_logo_url = logo_url
                    
                    db.update_restaurant_info(logo_url=new_logo_url)
                    st.success("✅ Logo güncellendi!")
                    st.rerun()
                except Exception as e:
                    st.error(f"❌ Hata: {e}")
    
    # ICON
    with col2:
        st.markdown("#### 🎯 Icon/Favicon")
        
        if restaurant.icon_url:
            st.markdown("**Mevcut Icon:**")
            try:
                st.image(restaurant.icon_url, width=100)
                st.caption(f"📁 {restaurant.icon_url}")
            except:
                st.caption(f"📁 {restaurant.icon_url}")
        
        with st.form("icon_form"):
            icon_file = st.file_uploader(
                "Yeni Icon Yükle",
                type=['png', 'jpg', 'jpeg', 'ico', 'svg', 'webp'],
                help="Önerilen boyut: 64x64 px veya 128x128 px"
            )
            icon_url = st.text_input(
                "veya Icon URL",
                value="" if icon_file else (restaurant.icon_url or ""),
                help="Dış kaynaklı icon URL'si"
            )
            delete_icon = st.checkbox("🗑️ Icon'u Sil")
            
            submit_icon = st.form_submit_button("💾 Icon Güncelle", use_container_width=True)
            
            if submit_icon:
                try:
                    new_icon_url = None
                    
                    if delete_icon:
                        # Delete old icon file if exists
                        if restaurant.icon_url and restaurant.icon_url.startswith("static/"):
                            if os.path.exists(restaurant.icon_url):
                                os.remove(restaurant.icon_url)
                        new_icon_url = None
                    elif icon_file:
                        # Upload new icon
                        upload_dir = "static/images/brand"
                        os.makedirs(upload_dir, exist_ok=True)
                        
                        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                        file_extension = icon_file.name.split('.')[-1]
                        filename = f"icon_{timestamp}.{file_extension}"
                        filepath = os.path.join(upload_dir, filename)
                        
                        with open(filepath, 'wb') as f:
                            f.write(icon_file.getbuffer())
                        
                        new_icon_url = filepath
                        st.success(f"📸 Icon yüklendi: {filename}")
                    elif icon_url:
                        new_icon_url = icon_url
                    
                    db.update_restaurant_info(icon_url=new_icon_url)
                    st.success("✅ Icon güncellendi!")
                    st.rerun()
                except Exception as e:
                    st.error(f"❌ Hata: {e}")

# ========================
# TAB 3: CONTACT INFO
# ========================
with tab3:
    st.markdown("### 📞 İletişim Bilgileri")
    
    with st.form("contact_form"):
        phone = st.text_input(
            "📱 Telefon",
            value=restaurant.phone or "",
            help="Örn: +90 212 XXX XX XX"
        )
        
        email = st.text_input(
            "📧 Email",
            value=restaurant.email or "",
            help="İletişim email adresi"
        )
        
        address = st.text_area(
            "📍 Adres",
            value=restaurant.address or "",
            height=100,
            help="Tam adres bilgisi"
        )
        
        submit_contact = st.form_submit_button("💾 Kaydet", type="primary", use_container_width=True)
        
        if submit_contact:
            try:
                db.update_restaurant_info(
                    phone=phone,
                    email=email,
                    address=address
                )
                st.success("✅ İletişim bilgileri güncellendi!")
                st.balloons()
                st.rerun()
            except Exception as e:
                st.error(f"❌ Hata: {e}")

# ========================
# TAB 4: SOCIAL MEDIA
# ========================
with tab4:
    st.markdown("### 🌐 Sosyal Medya Linkleri")
    
    with st.form("social_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            instagram = st.text_input(
                "📷 Instagram",
                value=social_media.get('instagram', ''),
                help="Tam URL: https://instagram.com/username"
            )
            
            facebook = st.text_input(
                "👥 Facebook",
                value=social_media.get('facebook', ''),
                help="Tam URL: https://facebook.com/page"
            )
        
        with col2:
            twitter = st.text_input(
                "🐦 Twitter/X",
                value=social_media.get('twitter', ''),
                help="Tam URL: https://twitter.com/username"
            )
            
            youtube = st.text_input(
                "📺 YouTube",
                value=social_media.get('youtube', ''),
                help="Tam URL: https://youtube.com/@channel"
            )
        
        submit_social = st.form_submit_button("💾 Kaydet", type="primary", use_container_width=True)
        
        if submit_social:
            try:
                new_social_media = {
                    'instagram': instagram,
                    'facebook': facebook,
                    'twitter': twitter,
                    'youtube': youtube
                }
                db.update_restaurant_info(
                    social_media=json.dumps(new_social_media, ensure_ascii=False)
                )
                st.success("✅ Sosyal medya linkleri güncellendi!")
                st.balloons()
                st.rerun()
            except Exception as e:
                st.error(f"❌ Hata: {e}")

# Preview section
st.markdown("---")
st.markdown("### 👁️ Önizleme")

col1, col2, col3 = st.columns([2, 1, 2])

with col1:
    st.markdown("#### 🇹🇷 Türkçe")
    if restaurant.logo_url:
        try:
            st.image(restaurant.logo_url, width=150)
        except:
            st.caption("Logo yüklenemedi")
    st.markdown(f"**{restaurant.name_tr}**")
    st.caption(restaurant.about_tr or "Açıklama yok")
    if restaurant.phone:
        st.caption(f"📱 {restaurant.phone}")
    if restaurant.email:
        st.caption(f"📧 {restaurant.email}")

with col2:
    if restaurant.icon_url:
        try:
            st.image(restaurant.icon_url, width=80)
        except:
            st.caption("Icon yüklenemedi")

with col3:
    st.markdown("#### 🇬🇧 English")
    st.markdown(f"**{restaurant.name_en}**")
    st.caption(restaurant.about_en or "No description")

# ========================
# TAB 5: AI ASSISTANT
# ========================
with tab5:
    st.markdown("### 🤖 AI Asistan Ayarları")
    st.info("💡 AI asistanın müşterilere gösterdiği karşılama mesajını özelleştirin.")
    
    with st.form("ai_settings_form"):
        st.markdown("#### 🇹🇷 Türkçe Karşılama Mesajı")
        ai_welcome_tr = st.text_area(
            "Türkçe Mesaj",
            value=restaurant.ai_welcome_message_tr or """🍕 **{restaurant_name}'ya Hoş Geldiniz!** 🍝

Ben sizin AI menü asistanınızım. Size yardımcı olmak için buradayım!

**Yapabileceklerim:**
- 🔍 Menüden öneri sunmak
- ❓ Sorularınızı cevaplamak
- 🌱 Vejetaryen/vegan seçenekleri göstermek
- 🌶️ Acılık seviyelerini açıklamak
- 🥜 Alerjen bilgileri vermek

**Örnek Sorular:**
- "Vejetaryen ne var?"
- "Acı pizzalarınız var mı?"
- "Fıstık alerjim var, ne önerirsiniz?"
- "100 TL altında ne yiyebilirim?"

Ne istersiniz? 😊""",
            height=350,
            help="Müşterilerin AI asistanı ilk açtığında göreceği mesaj. {restaurant_name} değişkenini kullanabilirsiniz."
        )
        
        st.markdown("---")
        st.markdown("#### 🇬🇧 English Welcome Message")
        ai_welcome_en = st.text_area(
            "English Message",
            value=restaurant.ai_welcome_message_en or """🍕 **Welcome to {restaurant_name}!** 🍝

I'm your AI menu assistant, here to help!

**I can help you with:**
- 🔍 Menu recommendations
- ❓ Answering questions
- 🌱 Vegetarian/vegan options
- 🌶️ Spiciness levels
- 🥜 Allergen information

**Example questions:**
- "What vegetarian options do you have?"
- "Do you have spicy pizzas?"
- "I'm allergic to nuts, what do you recommend?"
- "What can I eat under 100 TL?"

What would you like? 😊""",
            height=350,
            help="Welcome message customers see when opening AI assistant. You can use {restaurant_name} variable."
        )
        
        st.markdown("---")
        
        col1, col2 = st.columns([3, 1])
        with col1:
            st.caption("💡 **İpucu:** Mesajlarınızda {restaurant_name} kullanarak restoran adını dinamik olarak ekleyebilirsiniz.")
        
        with col2:
            submitted = st.form_submit_button(
                "💾 Kaydet",
                type="primary",
                use_container_width=True
            )
        
        if submitted:
            try:
                # Update database
                db.update_restaurant_info(
                    ai_welcome_message_tr=ai_welcome_tr,
                    ai_welcome_message_en=ai_welcome_en
                )
                st.success("✅ AI asistan ayarları güncellendi!")
                st.rerun()
            except Exception as e:
                st.error(f"❌ Hata: {str(e)}")
    
    # Preview section
    st.markdown("---")
    st.markdown("### 👁️ Önizleme")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### 🇹🇷 Türkçe Önizleme")
        preview_tr = (restaurant.ai_welcome_message_tr or ai_welcome_tr).replace(
            "{restaurant_name}", 
            restaurant.name_tr
        )
        st.markdown(
            f'<div style="background: #f0f2f6; padding: 1rem; border-radius: 10px; border-left: 4px solid #667eea;">{preview_tr}</div>',
            unsafe_allow_html=True
        )
    
    with col2:
        st.markdown("#### 🇬🇧 English Preview")
        preview_en = (restaurant.ai_welcome_message_en or ai_welcome_en).replace(
            "{restaurant_name}", 
            restaurant.name_en
        )
        st.markdown(
            f'<div style="background: #f0f2f6; padding: 1rem; border-radius: 10px; border-left: 4px solid #764ba2;">{preview_en}</div>',
            unsafe_allow_html=True
        )

# Footer
st.markdown("---")
st.caption(f"Son güncelleme: {restaurant.updated_at.strftime('%d.%m.%Y %H:%M') if restaurant.updated_at else 'N/A'}")

# Close database
db.close()
