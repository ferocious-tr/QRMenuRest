"""
Table Management Page - Manage tables and orders
Admin only access - requires authentication through admin.py
"""

import streamlit as st
import os
from database.db_manager import get_db
from database.models import Table
from utils.session_manager import init_session_state
from utils.page_navigation import show_admin_navigation, hide_default_sidebar
from datetime import datetime

# Page config
st.set_page_config(page_title="Masa Yönetimi", page_icon="🏓", layout="wide")

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
    .table-card {
        border: 3px solid #ddd;
        border-radius: 15px;
        padding: 1.5rem;
        margin: 1rem 0;
        text-align: center;
        transition: all 0.3s;
    }
    .table-available {
        background: #d4edda;
        border-color: #28a745;
    }
    .table-occupied {
        background: #f8d7da;
        border-color: #dc3545;
    }
    .table-reserved {
        background: #fff3cd;
        border-color: #ffc107;
    }
    .table-cleaning {
        background: #d1ecf1;
        border-color: #17a2b8;
    }
    .table-number {
        font-size: 2.5rem;
        font-weight: bold;
    }
    .order-card {
        background: white;
        border: 2px solid #f0f2f6;
        border-radius: 10px;
        padding: 1rem;
        margin: 0.5rem 0;
    }
</style>
""", unsafe_allow_html=True)

def get_table_status_class(status):
    """Get CSS class for table status"""
    return f"table-{status}"

def get_table_status_emoji(status):
    """Get emoji for table status"""
    emojis = {
        'available': '✅',
        'occupied': '🔴',
        'reserved': '📅',
        'cleaning': '🧹'
    }
    return emojis.get(status, '❓')

def show_table_details(table, db):
    """Show detailed information about a table"""
    st.markdown(f"### 🏓 Masa {table.table_number} Detayları")
    
    col1, col2, col3 = st.columns([2, 2, 1])
    
    with col1:
        st.markdown(f"""
        **Durum:** {get_table_status_emoji(table.status)} {table.status}  
        **Kapasite:** {table.capacity} kişi  
        **Son Güncelleme:** {table.updated_at.strftime('%H:%M')}
        """)
    
    with col2:
        # Status update
        status_options = ['available', 'occupied', 'reserved', 'cleaning']
        status_labels = {
            'available': '✅ Müsait',
            'occupied': '🔴 Dolu',
            'reserved': '📅 Rezerve',
            'cleaning': '🧹 Temizleniyor'
        }
        
        new_status = st.selectbox(
            "Durumu Değiştir",
            status_options,
            index=status_options.index(table.status),
            format_func=lambda x: status_labels.get(x, x),
            key=f"table_status_{table.id}"
        )
        
        if new_status != table.status:
            if st.button("✔️ Güncelle", key=f"update_table_{table.id}"):
                db.update_table_status(table.id, new_status)
                st.success("Masa durumu güncellendi!")
                st.rerun()
    
    with col3:
        # Show QR Code
        if table.qr_code and os.path.exists(table.qr_code):
            st.markdown("**QR Kod:**")
            st.image(table.qr_code, width=150)
            
            # Download button for QR code
            with open(table.qr_code, 'rb') as qr_file:
                st.download_button(
                    label="📥 İndir",
                    data=qr_file.read(),
                    file_name=f"masa_{table.table_number}_qr.png",
                    mime="image/png",
                    use_container_width=True,
                    key=f"download_qr_{table.id}"
                )
        else:
            st.warning("QR kod yok")
            if st.button("🔄 QR Oluştur", key=f"gen_qr_{table.id}"):
                from utils.qr_utils import generate_table_qr
                qr_path = generate_table_qr(table.table_number)
                
                # Update table with QR path
                fresh_table = db.session.query(Table).get(table.id)
                if fresh_table:
                    fresh_table.qr_code = qr_path
                    db.session.commit()
                    st.success("QR kod oluşturuldu!")
                    st.rerun()
    
    # Show orders for this table
    st.markdown("#### 📋 Bugünün Siparişleri")
    orders = db.get_today_orders_by_table(table.id)
    
    if not orders:
        st.info("Bu masa için bugün henüz sipariş yok.")
    else:
        st.markdown(f"**Toplam {len(orders)} sipariş**")
        
        # Show all orders (newest first)
        for order in reversed(orders):
            # Status badge
            status_config = {
                'pending': {'icon': '⏳', 'label': 'Bekliyor', 'color': '#FFA500'},
                'preparing': {'icon': '👨‍🍳', 'label': 'Hazırlanıyor', 'color': '#2196F3'},
                'ready': {'icon': '✅', 'label': 'Hazır', 'color': '#4CAF50'},
                'served': {'icon': '🍽️', 'label': 'Servis Edildi', 'color': '#9C27B0'},
                'paid': {'icon': '💰', 'label': 'Ödendi', 'color': '#28a745'},
                'cancelled': {'icon': '❌', 'label': 'İptal', 'color': '#dc3545'}
            }
            
            status_info = status_config.get(order.status, {'icon': '❓', 'label': order.status, 'color': '#888'})
            
            with st.expander(
                f"{status_info['icon']} {order.order_number} - {status_info['label']} ({order.created_at.strftime('%d.%m.%Y %H:%M')})", 
                expanded=(order.status in ['pending', 'preparing', 'ready'])
            ):
                col_a, col_b = st.columns(2)
                
                with col_a:
                    st.markdown(f"""
                    **Sipariş No:** {order.order_number}  
                    **Durum:** {status_info['icon']} {status_info['label']}  
                    **Sipariş Zamanı:** {order.created_at.strftime('%d.%m.%Y %H:%M')}  
                    **Toplam:** {order.total_amount:.2f} ₺
                    """)
                    
                    # Show timing info if available
                    if order.prepared_at:
                        st.caption(f"👨‍🍳 Hazırlandı: {order.prepared_at.strftime('%H:%M')}")
                    if order.served_at:
                        st.caption(f"🍽️ Servis Edildi: {order.served_at.strftime('%H:%M')}")
                    if order.paid_at:
                        st.caption(f"💰 Ödendi: {order.paid_at.strftime('%H:%M')}")
                
                with col_b:
                    # Order items
                    items = db.get_order_items(order.id)
                    st.markdown("**Ürünler:**")
                    for item in items:
                        st.write(f"• {item.quantity}x {item.menu_item.name} ({item.subtotal:.2f} ₺)")
                    
                    if order.special_requests:
                        st.info(f"💬 **Not:** {order.special_requests}")
                
                # Quick actions (only for active orders)
                if order.status in ['pending', 'preparing', 'ready', 'served']:
                    st.markdown("---")
                    col1, col2, col3, col4 = st.columns(4)
                    
                    with col1:
                        if order.status == 'pending':
                            if st.button("👨‍🍳 Hazırlamaya Başla", key=f"start_{order.id}", use_container_width=True):
                                db.update_order_status(order.id, 'preparing')
                                st.rerun()
                    
                    with col2:
                        if order.status == 'preparing':
                            if st.button("✅ Hazır", key=f"ready_{order.id}", use_container_width=True):
                                db.update_order_status(order.id, 'ready')
                                st.rerun()
                    
                    with col3:
                        if order.status == 'ready':
                            if st.button("🍽️ Servis Et", key=f"serve_{order.id}", use_container_width=True):
                                db.update_order_status(order.id, 'served')
                                st.rerun()
                    
                    with col4:
                        if order.status == 'served':
                            if st.button("💰 Ödendi", key=f"paid_{order.id}", use_container_width=True):
                                db.update_order_status(order.id, 'paid')
                                st.rerun()

def show_table_grid(tables, db):
    """Show table grid view"""
    st.markdown("## 🏓 Masa Görünümü")
    
    # Filter options
    col1, col2 = st.columns([1, 3])
    
    with col1:
        filter_status = st.selectbox(
            "Filtre",
            ["Tümü", "Müsait", "Dolu", "Rezerve", "Temizleniyor"],
            key="table_filter"
        )
    
    with col2:
        st.markdown("")  # Spacing
    
    # Apply filter
    status_map = {
        "Müsait": "available",
        "Dolu": "occupied",
        "Rezerve": "reserved",
        "Temizleniyor": "cleaning"
    }
    
    if filter_status != "Tümü":
        filtered_tables = [t for t in tables if t.status == status_map[filter_status]]
    else:
        filtered_tables = tables
    
    st.info(f"📊 {len(filtered_tables)} masa gösteriliyor")
    
    # Display tables in grid
    cols_per_row = 4
    rows = [filtered_tables[i:i+cols_per_row] for i in range(0, len(filtered_tables), cols_per_row)]
    
    for row in rows:
        cols = st.columns(cols_per_row)
        for idx, table in enumerate(row):
            with cols[idx]:
                status_class = get_table_status_class(table.status)
                emoji = get_table_status_emoji(table.status)
                
                st.markdown(f"""
                <div class="table-card {status_class}">
                    <div style="font-size: 3rem;">{emoji}</div>
                    <div class="table-number">{table.table_number}</div>
                    <div style="margin: 0.5rem 0;">👥 {table.capacity} kişi</div>
                    <div style="font-size: 0.9rem; color: #666;">{table.status}</div>
                </div>
                """, unsafe_allow_html=True)
                
                if st.button("📋 Detay", key=f"detail_{table.id}", use_container_width=True):
                    # Store selected table number for details tab
                    st.session_state['selected_table_for_details'] = table.table_number
                    st.rerun()

def show_quick_stats(db):
    """Show quick statistics"""
    tables = db.get_all_tables()
    active_orders = db.get_active_orders()
    
    col1, col2, col3, col4 = st.columns(4)
    
    available = len([t for t in tables if t.status == 'available'])
    occupied = len([t for t in tables if t.status == 'occupied'])
    reserved = len([t for t in tables if t.status == 'reserved'])
    
    with col1:
        st.metric("✅ Müsait Masa", available)
    
    with col2:
        st.metric("🔴 Dolu Masa", occupied)
    
    with col3:
        st.metric("📅 Rezerve", reserved)
    
    with col4:
        st.metric("📋 Aktif Sipariş", len(active_orders))

def main():
    """Main table management page"""
    st.title("🏓 Masa Yönetimi")
    
    # Get database
    db = get_db()
    
    # Show quick stats
    show_quick_stats(db)
    
    st.markdown("---")
    
    # Check if we should show a specific tab (for navigation from Masa Durumu)
    # Initialize active tab state
    if 'active_table_tab_index' not in st.session_state:
        st.session_state['active_table_tab_index'] = 0
    
    # If there's a selected table for details, show warning to guide user
    if 'selected_table_for_details' in st.session_state:
        selected_num = st.session_state['selected_table_for_details']
        st.info(f"📋 Masa {selected_num} detayları için **'Masa Detayları'** sekmesine gidin 👇")
    
    # Main tabs
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "📊 Masa Durumu", 
        "📋 Masa Detayları", 
        "➕ Yeni Masa",
        "✏️ Düzenle",
        "🗑️ Sil"
    ])
    
    with tab1:
        tables = db.get_all_tables()
        show_table_grid(tables, db)
    
    with tab2:
        st.markdown("### 🔍 Masa Seçin")
        
        table_numbers = [t.table_number for t in db.get_all_tables()]
        
        # Check if there's a pre-selected table from Masa Durumu tab
        default_table = None
        if 'selected_table_for_details' in st.session_state:
            default_table = st.session_state['selected_table_for_details']
            # Clear the selection after using it
            del st.session_state['selected_table_for_details']
        
        # Set default index
        default_index = 0
        if default_table and default_table in table_numbers:
            default_index = table_numbers.index(default_table)
        
        selected_table_num = st.selectbox(
            "Masa Numarası",
            table_numbers,
            index=default_index,
            key="select_table_detail"
        )
        
        if selected_table_num:
            table = db.get_table_by_number(selected_table_num)
            if table:
                show_table_details(table, db)
    
    with tab3:
        st.markdown("### ➕ Yeni Masa Ekle")
        
        with st.form("add_table_form"):
            col1, col2, col3 = st.columns(3)
            
            with col1:
                new_table_number = st.number_input(
                    "Masa Numarası *",
                    min_value=1,
                    max_value=100,
                    value=21,
                    key="new_table_num"
                )
            
            with col2:
                new_table_capacity = st.number_input(
                    "Kapasite *",
                    min_value=1,
                    max_value=20,
                    value=4,
                    key="new_table_capacity"
                )
            
            with col3:
                initial_status = st.selectbox(
                    "Başlangıç Durumu",
                    ["available", "reserved", "cleaning"],
                    format_func=lambda x: {
                        "available": "✅ Müsait",
                        "reserved": "📅 Rezerve",
                        "cleaning": "🧹 Temizleniyor"
                    }[x]
                )
            
            auto_generate_qr = st.checkbox("QR Kod Otomatik Oluştur", value=True)
            
            submitted = st.form_submit_button("➕ Masa Ekle", type="primary", use_container_width=True)
            
            if submitted:
                try:
                    # Check if table exists
                    existing = db.get_table_by_number(new_table_number)
                    if existing:
                        st.error(f"⚠️ Masa {new_table_number} zaten mevcut!")
                    else:
                        # Create QR code if requested
                        qr_path = None
                        if auto_generate_qr:
                            from utils.qr_utils import generate_table_qr
                            qr_path = generate_table_qr(new_table_number)
                        
                        # Create table
                        new_table = db.create_table(
                            table_number=new_table_number,
                            capacity=new_table_capacity,
                            qr_code=qr_path
                        )
                        
                        # Set initial status if not available
                        if initial_status != "available":
                            db.update_table_status(new_table.id, initial_status)
                        
                        st.success(f"✅ Masa {new_table_number} eklendi!")
                        if qr_path:
                            st.info(f"📱 QR kod oluşturuldu: {qr_path}")
                        st.balloons()
                        st.rerun()
                except Exception as e:
                    st.error(f"Hata: {e}")
    
    with tab4:
        # Edit table
        st.markdown("### ✏️ Masa Düzenle")
        
        tables = db.get_all_tables()
        
        if not tables:
            st.info("Henüz masa yok.")
        else:
            selected_table = st.selectbox(
                "Düzenlenecek Masayı Seçin",
                tables,
                format_func=lambda x: f"Masa {x.table_number} ({x.capacity} kişi) - {x.status}"
            )
            
            if selected_table:
                st.markdown(f"#### Masa {selected_table.table_number} Düzenleniyor")
                
                with st.form("edit_table_form"):
                    col1, col2, col3 = st.columns(3)
                    
                    with col1:
                        new_table_number = st.number_input(
                            "Masa Numarası",
                            min_value=1,
                            max_value=100,
                            value=selected_table.table_number,
                            key="edit_table_num",
                            help="Dikkat: Değiştirirseniz QR kod yeniden oluşturulmalı"
                        )
                    
                    with col2:
                        new_capacity = st.number_input(
                            "Kapasite",
                            min_value=1,
                            max_value=20,
                            value=selected_table.capacity,
                            key="edit_capacity"
                        )
                    
                    with col3:
                        new_status = st.selectbox(
                            "Durum",
                            ["available", "occupied", "reserved", "cleaning"],
                            index=["available", "occupied", "reserved", "cleaning"].index(selected_table.status),
                            format_func=lambda x: {
                                "available": "✅ Müsait",
                                "occupied": "🔴 Dolu",
                                "reserved": "📅 Rezerve",
                                "cleaning": "🧹 Temizleniyor"
                            }[x]
                        )
                    
                    regenerate_qr = st.checkbox(
                        "QR Kod Yeniden Oluştur",
                        value=new_table_number != selected_table.table_number
                    )
                    
                    submitted = st.form_submit_button("💾 Güncelle", type="primary", use_container_width=True)
                    
                    if submitted:
                        try:
                            # Check if new number conflicts with another table
                            if new_table_number != selected_table.table_number:
                                existing = db.get_table_by_number(new_table_number)
                                if existing:
                                    st.error(f"⚠️ Masa {new_table_number} zaten mevcut!")
                                    st.stop()
                            
                            # Refresh table from session to avoid detached instance
                            table_to_update = db.session.query(Table).get(selected_table.id)
                            
                            # Update table
                            table_to_update.table_number = new_table_number
                            table_to_update.capacity = new_capacity
                            table_to_update.status = new_status
                            
                            # Regenerate QR if requested
                            if regenerate_qr:
                                from utils.qr_utils import generate_table_qr
                                qr_path = generate_table_qr(new_table_number)
                                table_to_update.qr_code = qr_path
                                st.info(f"📱 QR kod yenilendi: {qr_path}")
                            
                            db.session.commit()
                            st.success("✅ Masa güncellendi!")
                            st.rerun()
                        except Exception as e:
                            st.error(f"Hata: {e}")
                            db.session.rollback()
    
    with tab5:
        # Delete tables
        st.markdown("### 🗑️ Masa Sil")
        st.warning("⚠️ Silme işlemi geri alınamaz! Aktif siparişi olan masalar silinemez.")
        
        tables = db.get_all_tables()
        
        if not tables:
            st.info("Henüz masa yok.")
        else:
            # Show tables that can be deleted (no active orders)
            deletable_tables = []
            for table in tables:
                active_orders = [o for o in db.get_orders_by_table(table.id) 
                               if o.status in ['pending', 'preparing', 'ready', 'served']]
                if not active_orders:
                    deletable_tables.append(table)
            
            if not deletable_tables:
                st.warning("⚠️ Tüm masaların aktif siparişi var, hiçbiri silinemiyor.")
            else:
                st.info(f"📊 {len(deletable_tables)} masa silinebilir durumda")
                
                selected_tables = st.multiselect(
                    "Silinecek Masaları Seçin",
                    deletable_tables,
                    format_func=lambda x: f"Masa {x.table_number} ({x.capacity} kişi) - {x.status}"
                )
                
                if selected_tables:
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        st.warning(f"⚠️ {len(selected_tables)} masa silinecek:")
                        for table in selected_tables:
                            st.write(f"• Masa {table.table_number}")
                    
                    with col2:
                        confirm_text = st.text_input(
                            "Onaylamak için 'SİL' yazın",
                            key="confirm_delete_tables"
                        )
                        
                        if confirm_text == "SİL":
                            if st.button("🗑️ Seçilenleri Sil", type="primary", use_container_width=True):
                                try:
                                    deleted_count = 0
                                    # Get table IDs first to avoid session issues
                                    table_ids = [table.id for table in selected_tables]
                                    
                                    for table_id in table_ids:
                                        # Re-fetch table from session
                                        table = db.session.query(Table).get(table_id)
                                        if table:
                                            # Delete QR code file if exists
                                            if table.qr_code:
                                                import os
                                                if os.path.exists(table.qr_code):
                                                    os.remove(table.qr_code)
                                            
                                            db.session.delete(table)
                                            deleted_count += 1
                                    
                                    db.session.commit()
                                    st.success(f"✅ {deleted_count} masa silindi!")
                                    st.rerun()
                                except Exception as e:
                                    st.error(f"Hata: {e}")
                                    db.session.rollback()
                        else:
                            st.info("👆 Silmek için yukarıya 'SİL' yazın")
    
    # Close database
    db.close()
    
    # Close database
    db.close()

if __name__ == "__main__":
    main()
