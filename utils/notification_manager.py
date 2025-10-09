"""
Notification Manager - Handle notifications for orders and events
"""

import os
from datetime import datetime
from typing import Optional, List, Dict
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import streamlit as st

class NotificationManager:
    """Manage notifications across different channels"""
    
    def __init__(self):
        """Initialize notification manager"""
        self.email_enabled = os.getenv('EMAIL_ENABLED', 'false').lower() == 'true'
        self.sms_enabled = os.getenv('SMS_ENABLED', 'false').lower() == 'true'
        
        # Email settings
        self.smtp_server = os.getenv('SMTP_SERVER', 'smtp.gmail.com')
        self.smtp_port = int(os.getenv('SMTP_PORT', '587'))
        self.email_from = os.getenv('EMAIL_FROM', '')
        self.email_password = os.getenv('EMAIL_PASSWORD', '')
        
        # SMS settings (placeholder - would need Twilio or similar)
        self.sms_api_key = os.getenv('SMS_API_KEY', '')
        self.sms_from = os.getenv('SMS_FROM', '')
    
    def notify_new_order(self, order_id: int, table_number: int, total_amount: float, items: List[Dict]) -> bool:
        """Notify about new order"""
        title = "🔔 Yeni Sipariş!"
        message = f"""
Masa {table_number}'den yeni sipariş geldi!

Sipariş No: {order_id}
Toplam: ₺{total_amount:.2f}

Ürünler:
"""
        for item in items:
            message += f"- {item['quantity']}x {item['name']}\n"
        
        # Show in-app notification
        if 'notifications' not in st.session_state:
            st.session_state.notifications = []
        
        st.session_state.notifications.append({
            'type': 'new_order',
            'title': title,
            'message': message,
            'timestamp': datetime.now(),
            'order_id': order_id
        })
        
        # Send email if enabled
        if self.email_enabled:
            self._send_email(
                subject=f"Yeni Sipariş - Masa {table_number}",
                body=message
            )
        
        # Send SMS if enabled
        if self.sms_enabled:
            self._send_sms(f"Yeni sipariş - Masa {table_number}, Tutar: ₺{total_amount:.2f}")
        
        return True
    
    def notify_order_status_change(self, order_id: int, table_number: int, old_status: str, new_status: str) -> bool:
        """Notify about order status change"""
        status_labels = {
            'pending': 'Bekliyor',
            'preparing': 'Hazırlanıyor',
            'ready': 'Hazır',
            'served': 'Servis Edildi',
            'paid': 'Ödendi',
            'cancelled': 'İptal Edildi'
        }
        
        title = "📊 Sipariş Durumu Değişti"
        message = f"""
Sipariş No: {order_id}
Masa: {table_number}
Durum: {status_labels.get(old_status, old_status)} → {status_labels.get(new_status, new_status)}
"""
        
        # Show in-app notification
        if 'notifications' not in st.session_state:
            st.session_state.notifications = []
        
        st.session_state.notifications.append({
            'type': 'status_change',
            'title': title,
            'message': message,
            'timestamp': datetime.now(),
            'order_id': order_id
        })
        
        # Notify customer for important status changes
        if new_status in ['ready', 'served']:
            customer_message = f"Masa {table_number} - Siparişiniz {status_labels.get(new_status, new_status)}!"
            
            if self.sms_enabled:
                self._send_sms(customer_message)
        
        return True
    
    def notify_low_stock(self, item_name: str, current_stock: int, threshold: int) -> bool:
        """Notify about low stock"""
        title = "⚠️ Düşük Stok Uyarısı"
        message = f"""
Ürün: {item_name}
Mevcut Stok: {current_stock}
Minimum Eşik: {threshold}

Stok yenilemesi gerekiyor!
"""
        
        # Show in-app notification
        if 'notifications' not in st.session_state:
            st.session_state.notifications = []
        
        st.session_state.notifications.append({
            'type': 'low_stock',
            'title': title,
            'message': message,
            'timestamp': datetime.now(),
            'priority': 'high'
        })
        
        # Send email for critical alerts
        if self.email_enabled:
            self._send_email(
                subject=f"Stok Uyarısı - {item_name}",
                body=message
            )
        
        return True
    
    def notify_table_call(self, table_number: int, request_type: str = "service") -> bool:
        """Notify about table calling for service"""
        request_labels = {
            'service': '📢 Garson Çağrısı',
            'bill': '💳 Hesap İsteme',
            'help': '🆘 Yardım'
        }
        
        title = request_labels.get(request_type, '🔔 Masa Çağrısı')
        message = f"Masa {table_number} - {title}"
        
        # Show in-app notification
        if 'notifications' not in st.session_state:
            st.session_state.notifications = []
        
        st.session_state.notifications.append({
            'type': 'table_call',
            'title': title,
            'message': message,
            'timestamp': datetime.now(),
            'table_number': table_number,
            'priority': 'high'
        })
        
        return True
    
    def _send_email(self, subject: str, body: str, to_email: Optional[str] = None) -> bool:
        """Send email notification"""
        if not self.email_enabled or not self.email_from or not self.email_password:
            return False
        
        try:
            # Use admin email if no recipient specified
            if not to_email:
                to_email = self.email_from
            
            # Create message
            msg = MIMEMultipart()
            msg['From'] = self.email_from
            msg['To'] = to_email
            msg['Subject'] = subject
            
            msg.attach(MIMEText(body, 'plain', 'utf-8'))
            
            # Send email
            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                server.starttls()
                server.login(self.email_from, self.email_password)
                server.send_message(msg)
            
            return True
        
        except Exception as e:
            print(f"Email send error: {e}")
            return False
    
    def _send_sms(self, message: str, to_phone: Optional[str] = None) -> bool:
        """Send SMS notification"""
        if not self.sms_enabled or not self.sms_api_key:
            return False
        
        # Placeholder for SMS integration
        # Would integrate with Twilio, AWS SNS, or similar service
        # Example with Twilio:
        # from twilio.rest import Client
        # client = Client(account_sid, auth_token)
        # client.messages.create(to=to_phone, from_=self.sms_from, body=message)
        
        print(f"SMS (would send): {message}")
        return True
    
    def get_unread_notifications(self) -> List[Dict]:
        """Get unread notifications"""
        if 'notifications' not in st.session_state:
            st.session_state.notifications = []
        
        if 'read_notifications' not in st.session_state:
            st.session_state.read_notifications = set()
        
        unread = []
        for i, notif in enumerate(st.session_state.notifications):
            if i not in st.session_state.read_notifications:
                unread.append({'index': i, **notif})
        
        return unread
    
    def mark_as_read(self, notification_index: int):
        """Mark notification as read"""
        if 'read_notifications' not in st.session_state:
            st.session_state.read_notifications = set()
        
        st.session_state.read_notifications.add(notification_index)
    
    def clear_all_notifications(self):
        """Clear all notifications"""
        st.session_state.notifications = []
        st.session_state.read_notifications = set()
    
    def get_notification_count(self) -> int:
        """Get count of unread notifications"""
        return len(self.get_unread_notifications())

# Global notification manager instance
_notification_manager = None

def get_notification_manager() -> NotificationManager:
    """Get or create notification manager singleton"""
    global _notification_manager
    
    if _notification_manager is None:
        _notification_manager = NotificationManager()
    
    return _notification_manager

def show_notifications_sidebar():
    """Show notifications in sidebar"""
    nm = get_notification_manager()
    unread = nm.get_unread_notifications()
    
    if unread:
        with st.sidebar:
            st.markdown("---")
            st.markdown(f"### 🔔 Bildirimler ({len(unread)})")
            
            for notif in unread[:5]:  # Show only latest 5
                with st.expander(f"{notif['title']} - {notif['timestamp'].strftime('%H:%M')}"):
                    st.write(notif['message'])
                    
                    col1, col2 = st.columns(2)
                    with col1:
                        if st.button("✓ Okundu", key=f"read_{notif['index']}"):
                            nm.mark_as_read(notif['index'])
                            st.rerun()
                    
                    with col2:
                        # Action buttons based on notification type
                        if notif['type'] == 'new_order' and 'order_id' in notif:
                            if st.button("👀 Görüntüle", key=f"view_{notif['index']}"):
                                st.session_state.view_order_id = notif['order_id']
                                st.switch_page("pages/4_📊_Admin_Dashboard.py")
            
            if len(unread) > 5:
                st.info(f"+{len(unread) - 5} bildirim daha...")
            
            if st.button("🗑️ Tümünü Temizle"):
                nm.clear_all_notifications()
                st.rerun()
