"""
Test page for notification sounds
"""

import streamlit as st
from utils.sound_manager import (
    play_notification_sound_v1,
    play_notification_sound_v2,
    play_notification_sound_v3,
    play_success_sound,
    play_alert_sound
)

st.set_page_config(page_title="Ses Testi", page_icon="🔊", layout="wide")

st.title("🔊 Bildirim Ses Sistemi Testi")

st.markdown("""
Bu sayfa bildirim seslerini test etmek içindir.
Butonlara tıklayarak farklı sesleri dinleyebilirsiniz.

**Not:** İlk sesi çalmadan önce tarayıcınızın ses iznini vermeniz gerekebilir.
""")

st.markdown("---")

col1, col2 = st.columns(2)

with col1:
    st.markdown("### 🔔 Bildirim Sesleri")
    
    if st.button("▶️ Tek Ton Beep (v1)", use_container_width=True):
        st.info("Ses çalınıyor... 🔊")
        play_notification_sound_v1()
        st.success("✅ Ses çalındı!")
    
    st.caption("800 Hz sinüs dalgası, 0.5 saniye")
    
    st.markdown("---")
    
    if st.button("▶️ Çift Ton Beep (v2) - Varsayılan", use_container_width=True):
        st.info("Ses çalınıyor... 🔊")
        play_notification_sound_v2()
        st.success("✅ Ses çalındı!")
    
    st.caption("1000 Hz → 800 Hz, daha dikkat çekici")
    
    st.markdown("---")
    
    if st.button("▶️ Harici URL Ses (v3)", use_container_width=True):
        st.info("Ses çalınıyor... 🔊")
        play_notification_sound_v3()
        st.success("✅ Ses çalındı!")
    
    st.caption("⚠️ İnternet bağlantısı gerektirir")

with col2:
    st.markdown("### 🎵 Özel Sesler")
    
    if st.button("▶️ Başarı Melodisi", use_container_width=True):
        st.info("Melodi çalınıyor... 🎵")
        play_success_sound()
        st.success("✅ Melodi çalındı!")
    
    st.caption("C-E-G akor, üç nota")
    
    st.markdown("---")
    
    if st.button("▶️ Acil Uyarı", use_container_width=True):
        st.warning("Uyarı sesi çalınıyor... ⚠️")
        play_alert_sound()
        st.success("✅ Uyarı çalındı!")
    
    st.caption("Üç hızlı beep, acil durumlar için")

st.markdown("---")

st.markdown("### 📋 Test Sonuçları")

with st.expander("✅ Ses çalıyorsa"):
    st.success("""
    Harika! Ses sistemi düzgün çalışıyor.
    
    Admin Dashboard'da yeni sipariş geldiğinde otomatik olarak ses duyacaksınız.
    """)

with st.expander("❌ Ses çalmıyorsa"):
    st.error("""
    Lütfen şunları kontrol edin:
    
    1. **Tarayıcı ses izni:** Tarayıcı ses çalmak için izin istiyor mu?
    2. **Bilgisayar sesi:** Ses açık mı? Volume kontrolü yapın
    3. **Tarayıcı konsolu:** F12 tuşuna basın, Console sekmesinde hata var mı?
    4. **Farklı tarayıcı:** Chrome, Edge veya Firefox deneyin
    5. **HTTPS:** Bazı tarayıcılar ses için HTTPS gerektirir
    """)

st.markdown("---")

st.info("""
💡 **İpucu:** Admin Dashboard'da bu sesler yeni sipariş geldiğinde otomatik çalar.
""")

# Debug info
if st.checkbox("🔧 Debug Bilgilerini Göster"):
    st.json({
        "Streamlit Version": st.__version__,
        "Components Available": True,
        "Sound Manager": "Loaded",
        "Default Sound": "play_notification_sound_v2 (Dual-tone beep)"
    })
