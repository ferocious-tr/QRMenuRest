"""
Notifications Center - View and manage all notifications
Admin only access - requires authentication through admin.py
"""

import streamlit as st
from utils.notification_manager import get_notification_manager, show_notifications_sidebar
from utils.session_manager import init_session_state
from utils.page_navigation import show_admin_navigation, hide_default_sidebar
from datetime import datetime, timedelta

# Page config
st.set_page_config(page_title="Bildirimler", page_icon="🔔", layout="wide")

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

# Custom CSS
st.markdown("""
<style>
    .notification-card {
        background: white;
        border-radius: 12px;
        padding: 1.5rem;
        margin: 0.5rem 0;
        box-shadow: 0 2px 6px rgba(0,0,0,0.08);
        border-left: 4px solid #667eea;
    }
    .notification-high {
        border-left-color: #f56565;
    }
    .notification-medium {
        border-left-color: #ed8936;
    }
    .notification-low {
        border-left-color: #48bb78;
    }
</style>
""", unsafe_allow_html=True)

def main():
    """Main notifications page"""
    st.title("🔔 Bildirim Merkezi")
    
    nm = get_notification_manager()
    
    # Header with stats and actions
    col1, col2, col3, col4 = st.columns([2, 2, 2, 1])
    
    with col1:
        st.metric("Toplam Bildirim", len(st.session_state.get('notifications', [])))
    
    with col2:
        unread_count = nm.get_notification_count()
        st.metric("Okunmamış", unread_count)
    
    with col3:
        # Calculate today's notifications
        today_count = 0
        for notif in st.session_state.get('notifications', []):
            if notif['timestamp'].date() == datetime.now().date():
                today_count += 1
        st.metric("Bugün", today_count)
    
    with col4:
        if st.button("🗑️ Tümünü Temizle", type="secondary"):
            if st.session_state.get('confirm_clear', False):
                nm.clear_all_notifications()
                st.success("✅ Tüm bildirimler temizlendi")
                st.session_state.confirm_clear = False
                st.rerun()
            else:
                st.session_state.confirm_clear = True
                st.warning("⚠️ Tekrar tıklayın")
    
    st.markdown("---")
    
    # Filter tabs
    tab1, tab2, tab3, tab4 = st.tabs([
        "📬 Tümü",
        "🔴 Okunmamış",
        "⚙️ Ayarlar",
        "📊 İstatistikler"
    ])
    
    with tab1:
        # Show all notifications
        all_notifications = st.session_state.get('notifications', [])
        
        if not all_notifications:
            st.info("📭 Henüz bildirim yok")
        else:
            # Group by date
            notifications_by_date = {}
            for i, notif in enumerate(all_notifications):
                date_key = notif['timestamp'].date()
                if date_key not in notifications_by_date:
                    notifications_by_date[date_key] = []
                notifications_by_date[date_key].append({'index': i, **notif})
            
            # Display by date groups
            for date_key in sorted(notifications_by_date.keys(), reverse=True):
                # Date header
                if date_key == datetime.now().date():
                    date_label = "🕐 Bugün"
                elif date_key == datetime.now().date() - timedelta(days=1):
                    date_label = "📅 Dün"
                else:
                    date_label = f"📅 {date_key.strftime('%d %B %Y')}"
                
                st.markdown(f"### {date_label}")
                
                # Show notifications for this date
                for notif in notifications_by_date[date_key]:
                    is_read = notif['index'] in st.session_state.get('read_notifications', set())
                    priority = notif.get('priority', 'low')
                    
                    col1, col2 = st.columns([6, 1])
                    
                    with col1:
                        with st.container():
                            # Notification header
                            status_icon = "✅" if is_read else "🔴"
                            st.markdown(f"**{status_icon} {notif['title']}** - {notif['timestamp'].strftime('%H:%M')}")
                            
                            # Notification body
                            st.write(notif['message'])
                            
                            # Metadata
                            metadata = []
                            if 'order_id' in notif:
                                metadata.append(f"Sipariş: #{notif['order_id']}")
                            if 'table_number' in notif:
                                metadata.append(f"Masa: {notif['table_number']}")
                            
                            if metadata:
                                st.caption(" | ".join(metadata))
                    
                    with col2:
                        if not is_read:
                            if st.button("✓", key=f"mark_read_{notif['index']}", help="Okundu olarak işaretle"):
                                nm.mark_as_read(notif['index'])
                                st.rerun()
                    
                    st.markdown("---")
    
    with tab2:
        # Show only unread
        unread = nm.get_unread_notifications()
        
        if not unread:
            st.success("🎉 Tüm bildirimler okundu!")
        else:
            st.info(f"📬 {len(unread)} okunmamış bildirim")
            
            for notif in unread:
                with st.container():
                    col1, col2 = st.columns([5, 1])
                    
                    with col1:
                        st.markdown(f"**🔴 {notif['title']}**")
                        st.write(notif['message'])
                        st.caption(notif['timestamp'].strftime('%d.%m.%Y %H:%M'))
                    
                    with col2:
                        if st.button("✓", key=f"read_{notif['index']}"):
                            nm.mark_as_read(notif['index'])
                            st.rerun()
                
                st.markdown("---")
            
            if st.button("✅ Tümünü Okundu İşaretle", type="primary"):
                for notif in unread:
                    nm.mark_as_read(notif['index'])
                st.rerun()
    
    with tab3:
        st.markdown("## ⚙️ Bildirim Ayarları")
        
        # Notification preferences
        st.markdown("### 📧 Email Bildirimleri")
        
        email_enabled = st.checkbox(
            "Email bildirimlerini etkinleştir",
            value=nm.email_enabled,
            help="Yeni siparişler ve önemli olaylar için email gönder"
        )
        
        if email_enabled:
            col1, col2 = st.columns(2)
            
            with col1:
                email_from = st.text_input(
                    "Email Adresi",
                    value=nm.email_from,
                    placeholder="admin@restaurant.com"
                )
            
            with col2:
                email_password = st.text_input(
                    "Email Şifresi",
                    type="password",
                    placeholder="********"
                )
            
            st.info("💡 Gmail kullanıyorsanız, 'App Password' oluşturmanız gerekir")
        
        st.markdown("---")
        
        # SMS notifications
        st.markdown("### 📱 SMS Bildirimleri")
        
        sms_enabled = st.checkbox(
            "SMS bildirimlerini etkinleştir",
            value=nm.sms_enabled,
            help="Kritik durumlar için SMS gönder (Twilio gerektirir)"
        )
        
        if sms_enabled:
            st.warning("⚠️ SMS servisi henüz yapılandırılmamış. Twilio veya benzeri bir SMS API entegrasyonu gerekiyor.")
        
        st.markdown("---")
        
        # In-app notifications
        st.markdown("### 🔔 Uygulama İçi Bildirimler")
        
        st.checkbox("Yeni sipariş bildirimleri", value=True)
        st.checkbox("Sipariş durumu değişiklikleri", value=True)
        st.checkbox("Düşük stok uyarıları", value=True)
        st.checkbox("Masa çağrıları", value=True)
        
        st.markdown("---")
        
        if st.button("💾 Ayarları Kaydet", type="primary"):
            st.success("✅ Ayarlar kaydedildi!")
            st.info("💡 .env dosyasını manuel olarak güncellemeniz gerekir")
            
            st.code(f"""
# .env dosyasına ekleyin:
EMAIL_ENABLED={'true' if email_enabled else 'false'}
EMAIL_FROM={email_from if email_enabled else ''}
EMAIL_PASSWORD=your_password_here
SMS_ENABLED={'true' if sms_enabled else 'false'}
""")
    
    with tab4:
        st.markdown("## 📊 Bildirim İstatistikleri")
        
        all_notifications = st.session_state.get('notifications', [])
        
        if not all_notifications:
            st.info("Henüz istatistik yok")
        else:
            # Type distribution
            type_counts = {}
            for notif in all_notifications:
                notif_type = notif.get('type', 'unknown')
                type_counts[notif_type] = type_counts.get(notif_type, 0) + 1
            
            type_labels = {
                'new_order': '🆕 Yeni Sipariş',
                'status_change': '📊 Durum Değişikliği',
                'low_stock': '⚠️ Düşük Stok',
                'table_call': '📢 Masa Çağrısı',
                'unknown': '❓ Diğer'
            }
            
            st.markdown("### 📋 Bildirim Türleri")
            
            for notif_type, count in sorted(type_counts.items(), key=lambda x: x[1], reverse=True):
                label = type_labels.get(notif_type, notif_type)
                percentage = (count / len(all_notifications)) * 100
                st.progress(percentage / 100, text=f"{label}: {count} (%{percentage:.1f})")
            
            st.markdown("---")
            
            # Timeline
            st.markdown("### 📈 Zaman Çizelgesi (Son 7 Gün)")
            
            # Group by day
            daily_counts = {}
            for notif in all_notifications:
                date_key = notif['timestamp'].date()
                daily_counts[date_key] = daily_counts.get(date_key, 0) + 1
            
            # Show last 7 days
            for i in range(7):
                date_key = datetime.now().date() - timedelta(days=i)
                count = daily_counts.get(date_key, 0)
                
                if date_key == datetime.now().date():
                    label = "Bugün"
                elif date_key == datetime.now().date() - timedelta(days=1):
                    label = "Dün"
                else:
                    label = date_key.strftime('%d.%m')
                
                if count > 0:
                    bar_length = min(int((count / max(daily_counts.values())) * 30), 30)
                    bar = "█" * bar_length
                    st.text(f"{label:8} {bar} {count}")
                else:
                    st.text(f"{label:8} - 0")
    


if __name__ == "__main__":
    main()
