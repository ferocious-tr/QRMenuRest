"""
Cart Page - View and manage shopping cart
"""

import streamlit as st
from utils.session_manager import (
    init_session_state, get_cart_count, update_cart_quantity, 
    remove_from_cart, clear_cart, get_session_id, get_table_number
)
from utils.page_navigation import show_customer_navigation, hide_default_sidebar
from database.db_manager import get_db
from datetime import datetime
import time

# Import notification manager
try:
    from utils.notification_manager import get_notification_manager
    NOTIFICATIONS_ENABLED = True
except ImportError:
    NOTIFICATIONS_ENABLED = False

# Page config
st.set_page_config(page_title="Sepet", page_icon="🛒", layout="wide")

# Hide default sidebar
hide_default_sidebar()

# Initialize session
init_session_state()

# Show customer navigation
show_customer_navigation()

# Custom CSS
st.markdown("""
<style>
    .cart-item {
        background: white;
        border: 2px solid #f0f2f6;
        border-radius: 12px;
        padding: 1.5rem;
        margin: 1rem 0;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
    }
    .cart-summary {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border-radius: 15px;
        padding: 2rem;
        margin: 1rem 0;
    }
    .total-price {
        font-size: 2rem;
        font-weight: bold;
        color: white;
    }
    .empty-cart {
        text-align: center;
        padding: 3rem;
        color: #888;
    }
    .success-message {
        background: #d4edda;
        border: 2px solid #c3e6cb;
        color: #155724;
        padding: 1rem;
        border-radius: 10px;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

def display_cart_item(item, index):
    """Display a single cart item"""
    col1, col2, col3, col4 = st.columns([3, 1, 1, 1])
    
    with col1:
        st.markdown(f"### {item['item_name']}")
        if item.get('notes'):
            st.caption(f"📝 {item['notes']}")
    
    with col2:
        st.markdown(f"**{item['price']} ₺**")
    
    with col3:
        new_qty = st.number_input(
            "Adet",
            min_value=0,
            max_value=10,
            value=item['quantity'],
            key=f"cart_qty_{index}",
            label_visibility="collapsed"
        )
        
        if new_qty != item['quantity']:
            update_cart_quantity(index, new_qty)
            st.rerun()
    
    with col4:
        st.markdown(f"**{item['subtotal']:.2f} ₺**")
        if st.button("🗑️", key=f"remove_{index}", help="Sepetten Çıkar"):
            remove_from_cart(index)
            st.rerun()

def show_cart_summary():
    """Display cart summary"""
    if not st.session_state.cart:
        st.markdown("""
        <div class="empty-cart">
            <h2>🛒 Sepetiniz Boş</h2>
            <p>Menüden ürün ekleyerek başlayın!</p>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("📖 Menüye Git", type="primary", use_container_width=True):
            st.switch_page("pages/1_🍽️_Menu.py")
        return False
    
    return True

def confirm_order():
    """Process order confirmation"""
    if not st.session_state.cart:
        st.error("Sepetiniz boş!")
        return
    
    if not st.session_state.table_number:
        st.error("Masa numarası bulunamadı!")
        return
    
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
        
        # Send notification for new order
        if NOTIFICATIONS_ENABLED:
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
        
        db.close()
        
        # Clear cart
        clear_cart()
        
        return order.order_number
        
    except Exception as e:
        st.error(f"Sipariş oluşturulurken hata: {e}")
        return None

def show_order_history():
    """Show customer's order history with status tracking"""
    if not st.session_state.get('table_id'):
        return
    
    db = get_db()
    
    # Get active orders for this table (not paid or cancelled)
    from database.models import Order
    from sqlalchemy import and_
    
    active_orders = db.session.query(Order).filter(
        and_(
            Order.table_id == st.session_state.table_id,
            Order.status.in_(['pending', 'preparing', 'ready', 'served'])
        )
    ).order_by(Order.created_at.desc()).all()
    
    if not active_orders:
        return
    
    st.markdown("---")
    st.markdown("## 📋 Aktif Siparişlerim")
    
    # Status configuration
    status_config = {
        'pending': {'icon': '⏳', 'label': 'Bekliyor', 'color': '#FFA500', 'progress': 25},
        'preparing': {'icon': '👨‍🍳', 'label': 'Hazırlanıyor', 'color': '#2196F3', 'progress': 50},
        'ready': {'icon': '✅', 'label': 'Hazır', 'color': '#4CAF50', 'progress': 75},
        'served': {'icon': '🍽️', 'label': 'Servis Edildi', 'color': '#9C27B0', 'progress': 100}
    }
    
    for order in active_orders:
        status_info = status_config.get(order.status, {'icon': '❓', 'label': order.status, 'color': '#888', 'progress': 0})
        
        with st.expander(f"{status_info['icon']} Sipariş #{order.order_number} - {status_info['label']}", expanded=True):
            # Progress bar
            st.progress(status_info['progress'] / 100)
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.markdown(f"**Sipariş No:** {order.order_number}")
                st.caption(f"📅 {order.created_at.strftime('%d.%m.%Y %H:%M')}")
            
            with col2:
                st.markdown(f"**Durum:** {status_info['icon']} {status_info['label']}")
                if order.status == 'preparing':
                    st.caption("⏱️ Tahmini: 10-15 dakika")
                elif order.status == 'ready':
                    st.caption("🔔 Siparişiniz hazır!")
            
            with col3:
                st.markdown(f"**Toplam:** {order.total_amount:.2f} ₺")
                st.caption(f"🍽️ {len(order.items)} ürün")
            
            # Order items
            st.markdown("**Ürünler:**")
            for item in order.items:
                st.markdown(f"- {item.quantity}x {item.menu_item.name} ({item.subtotal:.2f} ₺)")
            
            if order.special_requests:
                st.info(f"💬 **Özel İstek:** {order.special_requests}")
    
    db.close()

def main():
    """Main cart page"""
    st.title("🛒 Sepetim & Siparişlerim")
    
    # Show order history first
    show_order_history()
    
    # Auto-refresh countdown - place before other content
    if st.session_state.get('table_id'):
        # Initialize refresh timer
        if 'cart_refresh_count' not in st.session_state:
            st.session_state.cart_refresh_count = 0
        
        # Show refresh status and trigger auto-refresh
        placeholder = st.empty()
        
        # Countdown from 30 to 0
        for remaining in range(30, 0, -1):
            with placeholder.container():
                st.caption(f"� Sipariş durumları {remaining} saniye sonra güncellenecek...")
            time.sleep(1)
        
        # Trigger refresh
        st.session_state.cart_refresh_count += 1
        st.rerun()
    
    # Then show current cart
    st.markdown("---")
    st.markdown("## 🛒 Sepet")
    
    # Check if cart has items
    if not show_cart_summary():
        return
    
    # Display cart items
    st.markdown("### 📝 Sipariş Detayları")
    
    for idx, item in enumerate(st.session_state.cart):
        with st.container():
            display_cart_item(item, idx)
            st.markdown("---")
    
    # Cart summary and actions
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("### 💬 Özel İstekler")
        special_requests = st.text_area(
            "Siparişinizle ilgili özel bir isteğiniz var mı?",
            placeholder="Örn: Ekstra sos, az tuzlu, vb...",
            key="special_requests",
            label_visibility="collapsed"
        )
    
    with col2:
        # Summary box
        st.markdown(f"""
        <div class="cart-summary">
            <h3>📊 Sipariş Özeti</h3>
            <p>Masa: <strong>{get_table_number()}</strong></p>
            <p>Ürün Sayısı: <strong>{get_cart_count()}</strong></p>
            <hr style="border-color: rgba(255,255,255,0.3);">
            <p class="total-price">Toplam: {st.session_state.cart_total:.2f} ₺</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Action buttons
    st.markdown("---")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("🗑️ Sepeti Temizle", use_container_width=True):
            clear_cart()
            st.rerun()
    
    with col2:
        if st.button("⬅️ Menüye Dön", use_container_width=True):
            st.switch_page("pages/1_🍽️_Menu.py")
    
    with col3:
        if st.button("✅ Siparişi Onayla", type="primary", use_container_width=True):
            with st.spinner("Sipariş oluşturuluyor..."):
                order_number = confirm_order()
                
                if order_number:
                    st.success("🎉 Siparişiniz Alındı!")
                    
                    # Show order confirmation
                    st.balloons()
                    
                    st.markdown(f"""
                    <div class="success-message">
                        <h3>✅ Sipariş Başarılı!</h3>
                        <p><strong>Sipariş No:</strong> {order_number}</p>
                        <p><strong>Masa:</strong> {get_table_number()}</p>
                        <p><strong>Toplam:</strong> {st.session_state.cart_total:.2f} ₺</p>
                        <p><strong>Tahmini Hazırlanma Süresi:</strong> 15-25 dakika</p>
                        <p style="margin-top: 1rem;">
                            Siparişiniz mutfağa iletildi. Hazır olduğunda size getireceğiz. 
                            Afiyet olsun! 🍕
                        </p>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    # Options after order
                    col_a, col_b = st.columns(2)
                    
                    with col_a:
                        if st.button("🏠 Ana Sayfa", use_container_width=True):
                            st.switch_page("app.py")
                    
                    with col_b:
                        if st.button("📖 Menüye Dön", use_container_width=True):
                            st.switch_page("pages/1_🍽️_Menu.py")
    
    # Tips section
    st.markdown("---")
    st.markdown("### 💡 Bilgi")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.info("⏱️ **Ortalama Hazırlanma Süresi**\n\n15-25 dakika")
    
    with col2:
        st.info("🍽️ **Servis**\n\nSiparişiniz masanıza getirilecek")
    
    with col3:
        st.info("❓ **Yardım**\n\nPersonelimize danışabilirsiniz")

if __name__ == "__main__":
    main()
