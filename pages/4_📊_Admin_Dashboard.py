"""
Admin Dashboard - Statistics and management overview
Admin only access - requires authentication through admin.py
"""

import streamlit as st
from database.db_manager import get_db
from database.models import Order
from utils.session_manager import init_session_state, toggle_admin_mode
from utils.page_navigation import show_admin_navigation, hide_default_sidebar
from utils.sound_manager import play_alert_sound as play_notification_sound
from datetime import datetime, timedelta
import pandas as pd
import time

# Page config
st.set_page_config(page_title="Admin Dashboard", page_icon="📊", layout="wide")

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
    .metric-card {
        background: white;
        border-radius: 15px;
        padding: 1.5rem;
        box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        text-align: center;
    }
    .metric-value {
        font-size: 2.5rem;
        font-weight: bold;
        color: #667eea;
    }
    .metric-label {
        font-size: 1rem;
        color: #666;
        margin-top: 0.5rem;
    }
    .status-badge {
        padding: 0.3rem 0.8rem;
        border-radius: 12px;
        font-size: 0.85rem;
        font-weight: bold;
    }
    .status-pending { background: #fff3cd; color: #856404; }
    .status-preparing { background: #cce5ff; color: #004085; }
    .status-ready { background: #d4edda; color: #155724; }
    .status-served { background: #d1ecf1; color: #0c5460; }
    .status-paid { background: #d4edda; color: #155724; }
</style>
""", unsafe_allow_html=True)

def show_metrics(db):
    """Display key metrics"""
    stats = db.get_daily_stats()
    active_orders = db.get_active_orders()
    tables = db.get_all_tables()
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-value">₺{stats['total_revenue']:.2f}</div>
            <div class="metric-label">📈 Bugünkü Ciro</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-value">{stats['total_orders']}</div>
            <div class="metric-label">📋 Toplam Sipariş</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-value">{len(active_orders)}</div>
            <div class="metric-label">🔄 Aktif Sipariş</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        occupied_tables = len([t for t in tables if t.status == 'occupied'])
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-value">{occupied_tables}/{len(tables)}</div>
            <div class="metric-label">🏓 Dolu Masa</div>
        </div>
        """, unsafe_allow_html=True)

def show_active_orders(db):
    """Display active orders"""
    st.markdown("## 📋 Aktif Siparişler")
    
    orders = db.get_active_orders()
    
    if not orders:
        st.info("✅ Şu anda aktif sipariş yok.")
        return
    
    for order in orders:
        with st.expander(f"🍽️ {order.order_number} - Masa {order.table.table_number}", expanded=True):
            col1, col2, col3 = st.columns([2, 2, 1])
            
            with col1:
                st.markdown(f"**Sipariş Zamanı:** {order.created_at.strftime('%H:%M')}")
                st.markdown(f"**Masa:** {order.table.table_number}")
                st.markdown(f"**Toplam:** {order.total_amount:.2f} ₺")
            
            with col2:
                # Order items
                items = db.get_order_items(order.id)
                st.markdown("**Ürünler:**")
                for item in items:
                    st.write(f"• {item.quantity}x {item.menu_item.name}")
                
                if order.special_requests:
                    st.caption(f"💬 Not: {order.special_requests}")
            
            with col3:
                # Status update
                status_options = ['pending', 'preparing', 'ready', 'served', 'paid']
                status_labels = {
                    'pending': '⏳ Bekliyor',
                    'preparing': '👨‍🍳 Hazırlanıyor',
                    'ready': '✅ Hazır',
                    'served': '🍽️ Servis Edildi',
                    'paid': '💰 Ödendi'
                }
                
                current_status = status_labels.get(order.status, order.status)
                st.markdown(f"**Durum:** {current_status}")
                
                new_status = st.selectbox(
                    "Durumu Güncelle",
                    status_options,
                    index=status_options.index(order.status),
                    format_func=lambda x: status_labels.get(x, x),
                    key=f"status_{order.id}"
                )
                
                if new_status != order.status:
                    if st.button("✔️ Güncelle", key=f"update_{order.id}"):
                        db.update_order_status(order.id, new_status)
                        st.success("Durum güncellendi!")
                        st.rerun()

def show_popular_items(db):
    """Display popular menu items"""
    st.markdown("## ⭐ Popüler Ürünler")
    
    popular = db.get_popular_items(limit=10)
    
    if not popular:
        st.info("Henüz sipariş verilen ürün yok.")
        return
    
    # Create DataFrame for better display
    data = []
    for item in popular:
        data.append({
            'Ürün': item.name,
            'Kategori': item.category.name,
            'Fiyat': f"{item.price} ₺",
            'Sipariş Sayısı': item.order_count,
            'Puan': f"{item.rating:.1f}" if item.rating > 0 else "Yok"
        })
    
    df = pd.DataFrame(data)
    st.dataframe(df, use_container_width=True, hide_index=True)

def show_table_overview(db):
    """Display table status overview"""
    st.markdown("## 🏓 Masa Durumu")
    
    tables = db.get_all_tables()
    
    # Group by status
    status_counts = {
        'available': 0,
        'occupied': 0,
        'reserved': 0,
        'cleaning': 0
    }
    
    for table in tables:
        status_counts[table.status] = status_counts.get(table.status, 0) + 1
    
    # Display counts
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("✅ Müsait", status_counts['available'])
    with col2:
        st.metric("🔴 Dolu", status_counts['occupied'])
    with col3:
        st.metric("📅 Rezerve", status_counts['reserved'])
    with col4:
        st.metric("🧹 Temizleniyor", status_counts['cleaning'])
    
    # Table grid
    st.markdown("### Masa Düzeni")
    
    cols_per_row = 5
    rows = [tables[i:i+cols_per_row] for i in range(0, len(tables), cols_per_row)]
    
    for row in rows:
        cols = st.columns(cols_per_row)
        for idx, table in enumerate(row):
            with cols[idx]:
                status_emoji = {
                    'available': '✅',
                    'occupied': '🔴',
                    'reserved': '📅',
                    'cleaning': '🧹'
                }
                
                emoji = status_emoji.get(table.status, '❓')
                st.markdown(f"""
                <div style="text-align: center; padding: 1rem; border: 2px solid #ddd; border-radius: 10px; margin: 0.5rem 0;">
                    <div style="font-size: 2rem;">{emoji}</div>
                    <div style="font-weight: bold;">Masa {table.table_number}</div>
                    <div style="font-size: 0.8rem; color: #666;">{table.status}</div>
                </div>
                """, unsafe_allow_html=True)

# Note: Menu Management has been moved to separate page: pages/10_�️_Menu_Management.py

def check_new_orders():
    """Check for new orders and show notifications with sound"""
    # Initialize last check time
    if 'last_order_check' not in st.session_state:
        st.session_state.last_order_check = datetime.now()
        st.session_state.last_order_count = 0
        return
    
    db = get_db()
    
    # Get orders created after last check
    new_orders_query = db.session.query(Order).filter(
        Order.created_at > st.session_state.last_order_check
    )
    new_orders_count = new_orders_query.count()
    
    if new_orders_count > 0:
        # Play notification sound
        play_notification_sound()
        
        # Show toast notification
        st.toast(f"🔔 {new_orders_count} yeni sipariş geldi!", icon="🔔")
        
        # Get the actual new orders for details
        orders = new_orders_query.all()
        
        # Show detailed notifications
        for order in orders:
            st.toast(f"📋 Sipariş #{order.order_number} - Masa {order.table.table_number}", icon="🍕")
    
    # Update last check time
    st.session_state.last_order_check = datetime.now()
    st.session_state.last_order_count = db.session.query(Order).count()
    
    db.close()

def main():
    """Main admin dashboard"""
    st.title("📊 Admin Dashboard")
    
    # Check for new orders at the beginning
    check_new_orders()
    
    # Get database
    db = get_db()
    
    # Show metrics
    show_metrics(db)
    
    st.markdown("---")
    
    # Main content tabs
    tab1, tab2, tab3 = st.tabs([
        "📋 Siparişler",
        "🏓 Masalar", 
        "⭐ Popüler Ürünler"
    ])
    
    with tab1:
        show_active_orders(db)
    
    with tab2:
        show_table_overview(db)
    
    with tab3:
        show_popular_items(db)
    
    # Close database
    db.close()
    
    # Auto-refresh countdown - place at the bottom
    st.markdown("---")
    
    # Initialize refresh counter
    if 'admin_refresh_count' not in st.session_state:
        st.session_state.admin_refresh_count = 0
    
    # Show refresh status and trigger auto-refresh
    placeholder = st.empty()
    
    # Countdown from 10 to 0
    for remaining in range(10, 0, -1):
        with placeholder.container():
            col1, col2 = st.columns([3, 1])
            with col1:
                st.caption(f"📅 {datetime.now().strftime('%d.%m.%Y %H:%M:%S')} - Admin Panel v2.0")
            with col2:
                st.caption(f"🔄 Yenileme: {remaining}s")
        time.sleep(1)
    
    # Trigger refresh
    st.session_state.admin_refresh_count += 1
    st.rerun()

if __name__ == "__main__":
    main()
