"""
Reports Page - Advanced analytics and reporting
Admin only access - requires authentication through admin.py
"""

import streamlit as st
from database.db_manager import get_db
from database.models import Order, OrderItem, MenuItem
from sqlalchemy import func
from utils.session_manager import init_session_state
from utils.page_navigation import show_admin_navigation, hide_default_sidebar
from datetime import datetime, timedelta
import pandas as pd
import io

# Page config
st.set_page_config(page_title="Raporlar", page_icon="📊", layout="wide")

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
    .report-card {
        background: white;
        border-radius: 15px;
        padding: 1.5rem;
        box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        margin: 1rem 0;
    }
    .metric-big {
        font-size: 2rem;
        font-weight: bold;
        color: #667eea;
    }
</style>
""", unsafe_allow_html=True)

def generate_sales_report(db, start_date, end_date):
    """Generate sales report for date range"""
    from sqlalchemy import func, and_
    from database.models import Order
    
    # Get orders in date range
    orders = db.session.query(Order).filter(
        and_(
            func.DATE(Order.created_at) >= start_date,
            func.DATE(Order.created_at) <= end_date
        )
    ).all()
    
    if not orders:
        return None
    
    # Calculate metrics
    total_orders = len(orders)
    total_revenue = sum(o.total_amount for o in orders if o.status == 'paid')
    avg_order_value = total_revenue / total_orders if total_orders > 0 else 0
    
    # Orders by status
    status_counts = {}
    for order in orders:
        status_counts[order.status] = status_counts.get(order.status, 0) + 1
    
    # Daily breakdown
    daily_data = {}
    for order in orders:
        date_key = order.created_at.date()
        if date_key not in daily_data:
            daily_data[date_key] = {'orders': 0, 'revenue': 0}
        daily_data[date_key]['orders'] += 1
        if order.status == 'paid':
            daily_data[date_key]['revenue'] += order.total_amount
    
    return {
        'total_orders': total_orders,
        'total_revenue': total_revenue,
        'avg_order_value': avg_order_value,
        'status_counts': status_counts,
        'daily_data': daily_data
    }

def generate_product_report(db):
    """Generate product performance report"""
    from sqlalchemy import func
    from database.models import MenuItem, OrderItem
    
    # Get product stats
    product_stats = db.session.query(
        MenuItem.name,
        MenuItem.category_id,
        MenuItem.price,
        func.count(OrderItem.id).label('order_count'),
        func.sum(OrderItem.quantity).label('total_quantity'),
        func.sum(OrderItem.subtotal).label('total_revenue')
    ).join(
        OrderItem, MenuItem.id == OrderItem.menu_item_id
    ).group_by(
        MenuItem.id
    ).order_by(
        func.sum(OrderItem.subtotal).desc()
    ).all()
    
    return product_stats

def export_to_excel(data, filename):
    """Export data to Excel"""
    output = io.BytesIO()
    
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        if isinstance(data, dict):
            for sheet_name, df in data.items():
                df.to_excel(writer, sheet_name=sheet_name, index=False)
        else:
            data.to_excel(writer, index=False)
    
    return output.getvalue()

def show_table_reports(db):
    """Show table reports with orders and export option"""
    st.markdown("## 🏓 Masa Raporları")
    
    # Initialize session state for table report dates (default: last 8 days)
    if 'table_report_start_date' not in st.session_state:
        st.session_state.table_report_start_date = datetime.now().date() - timedelta(days=7)
    if 'table_report_end_date' not in st.session_state:
        st.session_state.table_report_end_date = datetime.now().date()
    if 'table_last_quick_range' not in st.session_state:
        st.session_state.table_last_quick_range = "Son 7 Gün"
    
    # Date range selector - independent from main page
    st.markdown("### 📅 Tarih Aralığı Seçin")
    
    col_date1, col_date2, col_date3, col_date4 = st.columns([2, 2, 1, 1])
    
    with col_date3:
        quick_range = st.selectbox(
            "Hızlı Seçim",
            ["Özel", "Bugün", "Dün", "Son 7 Gün", "Son 30 Gün", "Bu Ay"],
            index=["Özel", "Bugün", "Dün", "Son 7 Gün", "Son 30 Gün", "Bu Ay"].index(st.session_state.table_last_quick_range) if st.session_state.table_last_quick_range in ["Özel", "Bugün", "Dün", "Son 7 Gün", "Son 30 Gün", "Bu Ay"] else 3,
            key="table_quick_range"
        )
        
        # Check if quick range changed
        if quick_range != st.session_state.table_last_quick_range and quick_range != "Özel":
            st.session_state.table_last_quick_range = quick_range
            
            # Apply quick range selection to session state
            if quick_range == "Bugün":
                st.session_state.table_report_start_date = datetime.now().date()
                st.session_state.table_report_end_date = datetime.now().date()
            elif quick_range == "Dün":
                yesterday = datetime.now().date() - timedelta(days=1)
                st.session_state.table_report_start_date = yesterday
                st.session_state.table_report_end_date = yesterday
            elif quick_range == "Son 7 Gün":
                st.session_state.table_report_start_date = datetime.now().date() - timedelta(days=7)
                st.session_state.table_report_end_date = datetime.now().date()
            elif quick_range == "Son 30 Gün":
                st.session_state.table_report_start_date = datetime.now().date() - timedelta(days=30)
                st.session_state.table_report_end_date = datetime.now().date()
            elif quick_range == "Bu Ay":
                st.session_state.table_report_start_date = datetime.now().date().replace(day=1)
                st.session_state.table_report_end_date = datetime.now().date()
            
            st.rerun()
    
    with col_date1:
        table_start_date = st.date_input(
            "Başlangıç Tarihi",
            value=st.session_state.table_report_start_date,
            max_value=datetime.now().date(),
            key="table_report_start"
        )
        # User manually changed date, set to "Özel"
        if table_start_date != st.session_state.table_report_start_date:
            st.session_state.table_last_quick_range = "Özel"
    
    with col_date2:
        table_end_date = st.date_input(
            "Bitiş Tarihi",
            value=st.session_state.table_report_end_date,
            max_value=datetime.now().date(),
            key="table_report_end"
        )
        # User manually changed date, set to "Özel"
        if table_end_date != st.session_state.table_report_end_date:
            st.session_state.table_last_quick_range = "Özel"
    
    # Auto-update session state when dates change
    st.session_state.table_report_start_date = table_start_date
    st.session_state.table_report_end_date = table_end_date
    
    # Use session state values for query
    query_start_date = st.session_state.table_report_start_date
    query_end_date = st.session_state.table_report_end_date
    
    st.markdown("---")
    
    # Table selector
    col1, col2 = st.columns([2, 1])
    
    with col1:
        tables = db.get_all_tables()
        table_options = ["Tüm Masalar"] + [f"Masa {t.table_number}" for t in tables]
        selected_table = st.selectbox("Masa Seçin", table_options, key="table_selector")
    
    with col2:
        st.metric("Seçilen Aralık", f"{(query_end_date - query_start_date).days + 1} gün")
    
    # Get table_id if specific table selected
    table_id = None
    if selected_table != "Tüm Masalar":
        table_num = int(selected_table.split(" ")[1])
        table = db.get_table_by_number(table_num)
        table_id = table.id if table else None
    
    # Get orders with the selected date range
    orders = db.get_orders_by_table_and_date_range(table_id, query_start_date, query_end_date)
    
    if not orders:
        st.info(f"📋 {selected_table} için {query_start_date.strftime('%d.%m.%Y')} - {query_end_date.strftime('%d.%m.%Y')} tarihleri arasında sipariş bulunamadı.")
        return
    
    # Summary metrics
    st.markdown("### 📊 Özet")
    col1, col2, col3, col4 = st.columns(4)
    
    total_revenue = sum(o.total_amount for o in orders if o.status == 'paid')
    avg_order = total_revenue / len(orders) if orders else 0
    
    with col1:
        st.metric("Toplam Sipariş", len(orders))
    
    with col2:
        st.metric("Toplam Ciro", f"₺{total_revenue:.2f}")
    
    with col3:
        st.metric("Ortalama Sipariş", f"₺{avg_order:.2f}")
    
    with col4:
        paid_orders = len([o for o in orders if o.status == 'paid'])
        st.metric("Ödenen Sipariş", paid_orders)
    
    st.markdown("---")
    
    # Orders table
    st.markdown("### 📋 Sipariş Detayları")
    
    # Prepare data for display and export
    orders_data = []
    for order in orders:
        # Get items
        items = db.get_order_items(order.id)
        items_list = ", ".join([f"{item.quantity}x {item.menu_item.name}" for item in items])
        
        orders_data.append({
            'Sipariş No': order.order_number,
            'Masa': order.table.table_number,
            'Tarih': order.created_at.strftime('%d.%m.%Y'),
            'Saat': order.created_at.strftime('%H:%M'),
            'Durum': order.status,
            'Ürünler': items_list,
            'Toplam (₺)': f"{order.total_amount:.2f}",
            'Özel İstek': order.special_requests if order.special_requests else '-'
        })
    
    orders_df = pd.DataFrame(orders_data)
    
    # Display table
    st.dataframe(orders_df, use_container_width=True, hide_index=True)
    
    # Excel export button
    st.markdown("---")
    st.markdown("### 📥 Excel Export")
    
    col1, col2, col3 = st.columns([2, 1, 1])
    
    with col1:
        st.info(f"📊 {len(orders)} sipariş Excel formatında indirilebilir")
    
    with col2:
        if st.button("📊 Excel İndir", type="primary", use_container_width=True, key="excel_export_btn"):
            # Create Excel file
            output = io.BytesIO()
            with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
                # Orders sheet
                orders_df.to_excel(writer, sheet_name='Siparişler', index=False)
                
                # Summary sheet
                summary_df = pd.DataFrame([{
                    'Başlangıç Tarihi': query_start_date.strftime('%d.%m.%Y'),
                    'Bitiş Tarihi': query_end_date.strftime('%d.%m.%Y'),
                    'Masa': selected_table,
                    'Toplam Sipariş': len(orders),
                    'Toplam Ciro (₺)': total_revenue,
                    'Ortalama Sipariş (₺)': avg_order,
                    'Ödenen Sipariş': paid_orders
                }])
                summary_df.to_excel(writer, sheet_name='Özet', index=False)
            
            excel_data = output.getvalue()
            
            filename = f"masa_raporu_{selected_table.replace(' ', '_')}_{query_start_date}_{query_end_date}.xlsx"
            
            st.download_button(
                label="💾 İndir",
                data=excel_data,
                file_name=filename,
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                use_container_width=True,
                key="excel_download_btn"
            )

def main():
    """Main reports page"""
    st.title("📊 Raporlar ve Analizler")
    
    # Get database
    db = get_db()
    
    # Main tabs
    tab1, tab2, tab3, tab4 = st.tabs([
        "💰 Satış Raporu",
        "🍽️ Ürün Performansı",
        "🏓 Masa Raporları",
        "📈 Grafikler"
    ])
    
    with tab1:
        st.markdown("## 💰 Satış Raporu")
        
        # Date range selector - inside Sales Report tab
        st.markdown("### 📅 Tarih Aralığı")
        
        # Initialize default dates in session state if not exists
        if 'sales_default_start' not in st.session_state:
            st.session_state.sales_default_start = datetime.now().date() - timedelta(days=7)
        if 'sales_default_end' not in st.session_state:
            st.session_state.sales_default_end = datetime.now().date()
        if 'sales_last_quick_range' not in st.session_state:
            st.session_state.sales_last_quick_range = "Son 7 Gün"
        
        col1, col2, col3 = st.columns([2, 2, 1])
        
        with col3:
            quick_range = st.selectbox(
                "Hızlı Seçim",
                ["Özel", "Bugün", "Dün", "Son 7 Gün", "Son 30 Gün", "Bu Ay"],
                index=["Özel", "Bugün", "Dün", "Son 7 Gün", "Son 30 Gün", "Bu Ay"].index(st.session_state.sales_last_quick_range) if st.session_state.sales_last_quick_range in ["Özel", "Bugün", "Dün", "Son 7 Gün", "Son 30 Gün", "Bu Ay"] else 3,
                key="sales_quick_input"
            )
            
            # Check if quick range changed
            if quick_range != st.session_state.sales_last_quick_range and quick_range != "Özel":
                st.session_state.sales_last_quick_range = quick_range
                
                # Update default dates based on quick selection
                if quick_range == "Bugün":
                    st.session_state.sales_default_start = datetime.now().date()
                    st.session_state.sales_default_end = datetime.now().date()
                elif quick_range == "Dün":
                    yesterday = datetime.now().date() - timedelta(days=1)
                    st.session_state.sales_default_start = yesterday
                    st.session_state.sales_default_end = yesterday
                elif quick_range == "Son 7 Gün":
                    st.session_state.sales_default_start = datetime.now().date() - timedelta(days=7)
                    st.session_state.sales_default_end = datetime.now().date()
                elif quick_range == "Son 30 Gün":
                    st.session_state.sales_default_start = datetime.now().date() - timedelta(days=30)
                    st.session_state.sales_default_end = datetime.now().date()
                elif quick_range == "Bu Ay":
                    st.session_state.sales_default_start = datetime.now().date().replace(day=1)
                    st.session_state.sales_default_end = datetime.now().date()
                
                st.rerun()
        
        with col1:
            start_date = st.date_input(
                "Başlangıç",
                value=st.session_state.sales_default_start,
                max_value=datetime.now().date(),
                key="sales_start_input"
            )
            # User manually changed date, set to "Özel"
            if start_date != st.session_state.sales_default_start:
                st.session_state.sales_last_quick_range = "Özel"
        
        with col2:
            end_date = st.date_input(
                "Bitiş",
                value=st.session_state.sales_default_end,
                max_value=datetime.now().date(),
                key="sales_end_input"
            )
            # User manually changed date, set to "Özel"
            if end_date != st.session_state.sales_default_end:
                st.session_state.sales_last_quick_range = "Özel"
        
        st.markdown("---")
        
        # Generate sales report
        sales_report = generate_sales_report(db, start_date, end_date)
        
        # Store in session state for other tabs
        st.session_state.sales_report = sales_report
        st.session_state.sales_start_date = start_date
        st.session_state.sales_end_date = end_date
        
        if not sales_report:
            st.warning(f"⚠️ {start_date.strftime('%d.%m.%Y')} - {end_date.strftime('%d.%m.%Y')} tarihleri arasında veri bulunamadı.")
        else:
            st.markdown("### 📊 Özet")
            
            # Key metrics
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.metric("Toplam Sipariş", sales_report['total_orders'])
            
            with col2:
                st.metric("Toplam Ciro", f"₺{sales_report['total_revenue']:.2f}")
            
            with col3:
                st.metric("Ortalama Sipariş", f"₺{sales_report['avg_order_value']:.2f}")
            
            with col4:
                completion_rate = (sales_report['status_counts'].get('paid', 0) / 
                                 sales_report['total_orders'] * 100 if sales_report['total_orders'] > 0 else 0)
                st.metric("Tamamlanma Oranı", f"%{completion_rate:.1f}")
            
            # Status breakdown
            st.markdown("### 📊 Sipariş Durumu")
            
            status_labels = {
                'pending': '⏳ Bekliyor',
                'preparing': '👨‍🍳 Hazırlanıyor',
                'ready': '✅ Hazır',
                'served': '🍽️ Servis Edildi',
                'paid': '💰 Ödendi',
                'cancelled': '❌ İptal'
            }
            
            status_df = pd.DataFrame([
                {'Durum': status_labels.get(k, k), 'Adet': v}
                for k, v in sales_report['status_counts'].items()
            ])
            
            col1, col2 = st.columns([2, 1])
            
            with col1:
                st.dataframe(status_df, use_container_width=True, hide_index=True)
            
            with col2:
                # Simple bar representation
                for status, count in sales_report['status_counts'].items():
                    percentage = (count / sales_report['total_orders'] * 100)
                    st.progress(percentage / 100, text=f"{status_labels.get(status, status)}: {count}")
            
            # Daily breakdown
            st.markdown("### 📅 Günlük Dağılım")
            
            daily_df = pd.DataFrame([
                {
                    'Tarih': date.strftime('%d.%m.%Y'),
                    'Sipariş Sayısı': data['orders'],
                    'Ciro (₺)': f"{data['revenue']:.2f}"
                }
                for date, data in sorted(sales_report['daily_data'].items())
            ])
            
            st.dataframe(daily_df, use_container_width=True, hide_index=True)
    
    with tab2:
        st.markdown("## 🍽️ Ürün Performansı")
        
        # Date range selector for product performance
        st.markdown("### 📅 Tarih Aralığı")
        
        # Initialize default dates in session state
        if 'product_default_start' not in st.session_state:
            st.session_state.product_default_start = datetime.now().date() - timedelta(days=30)
        if 'product_default_end' not in st.session_state:
            st.session_state.product_default_end = datetime.now().date()
        if 'product_last_quick_range' not in st.session_state:
            st.session_state.product_last_quick_range = "Son 30 Gün"
        
        col1, col2, col3 = st.columns([2, 2, 1])
        
        with col3:
            product_quick_range = st.selectbox(
                "Hızlı Seçim",
                ["Özel", "Bugün", "Dün", "Son 7 Gün", "Son 30 Gün", "Bu Ay"],
                index=["Özel", "Bugün", "Dün", "Son 7 Gün", "Son 30 Gün", "Bu Ay"].index(st.session_state.product_last_quick_range) if st.session_state.product_last_quick_range in ["Özel", "Bugün", "Dün", "Son 7 Gün", "Son 30 Gün", "Bu Ay"] else 4,
                key="product_quick_input"
            )
            
            # Check if quick range changed
            if product_quick_range != st.session_state.product_last_quick_range and product_quick_range != "Özel":
                st.session_state.product_last_quick_range = product_quick_range
                
                if product_quick_range == "Bugün":
                    st.session_state.product_default_start = datetime.now().date()
                    st.session_state.product_default_end = datetime.now().date()
                elif product_quick_range == "Dün":
                    yesterday = datetime.now().date() - timedelta(days=1)
                    st.session_state.product_default_start = yesterday
                    st.session_state.product_default_end = yesterday
                elif product_quick_range == "Son 7 Gün":
                    st.session_state.product_default_start = datetime.now().date() - timedelta(days=7)
                    st.session_state.product_default_end = datetime.now().date()
                elif product_quick_range == "Son 30 Gün":
                    st.session_state.product_default_start = datetime.now().date() - timedelta(days=30)
                    st.session_state.product_default_end = datetime.now().date()
                elif product_quick_range == "Bu Ay":
                    st.session_state.product_default_start = datetime.now().date().replace(day=1)
                    st.session_state.product_default_end = datetime.now().date()
                
                st.rerun()
        
        with col1:
            product_start_date = st.date_input(
                "Başlangıç",
                value=st.session_state.product_default_start,
                max_value=datetime.now().date(),
                key="product_start_input"
            )
            if product_start_date != st.session_state.product_default_start:
                st.session_state.product_last_quick_range = "Özel"
        
        with col2:
            product_end_date = st.date_input(
                "Bitiş",
                value=st.session_state.product_default_end,
                max_value=datetime.now().date(),
                key="product_end_input"
            )
            if product_end_date != st.session_state.product_default_end:
                st.session_state.product_last_quick_range = "Özel"
        
        st.markdown("---")
        
        # Get product stats with date filter
        product_stats = (db.session.query(
            MenuItem.name,
            MenuItem.category_id,
            MenuItem.price,
            func.count(OrderItem.id).label('order_count'),
            func.sum(OrderItem.quantity).label('total_quantity'),
            func.sum(OrderItem.subtotal).label('total_revenue')
        ).join(
            OrderItem, MenuItem.id == OrderItem.menu_item_id
        ).join(
            Order, OrderItem.order_id == Order.id
        ).filter(
            Order.created_at.between(product_start_date, product_end_date + timedelta(days=1))
        ).group_by(
            MenuItem.id
        ).order_by(
            func.sum(OrderItem.subtotal).desc()
        ).all())
        
        if not product_stats:
            st.info(f"📋 {product_start_date.strftime('%d.%m.%Y')} - {product_end_date.strftime('%d.%m.%Y')} tarihleri arasında ürün satışı yok.")
        else:
            # Top products
            st.markdown("### ⭐ En Çok Satanlar (Top 10)")
            
            top_products = product_stats[:10]
            
            top_df = pd.DataFrame([
                {
                    'Ürün': p.name,
                    'Sipariş Sayısı': p.order_count,
                    'Toplam Adet': p.total_quantity,
                    'Birim Fiyat': f"{p.price:.2f} ₺",
                    'Toplam Ciro': f"{p.total_revenue:.2f} ₺"
                }
                for p in top_products
            ])
            
            st.dataframe(top_df, use_container_width=True, hide_index=True)
            
            # All products
            st.markdown("### 📋 Tüm Ürünler")
            
            all_df = pd.DataFrame([
                {
                    'Ürün': p.name,
                    'Sipariş': p.order_count,
                    'Adet': p.total_quantity,
                    'Ciro (₺)': f"{p.total_revenue:.2f}"
                }
                for p in product_stats
            ])
            
            st.dataframe(all_df, use_container_width=True, hide_index=True)
    
    with tab3:
        # Masa Raporları - independent date selection
        show_table_reports(db)
    
    with tab4:
        st.markdown("## 📈 Grafiksel Analizler")
        
        # Date range selector for graphs
        st.markdown("### 📅 Tarih Aralığı")
        
        # Initialize default dates in session state
        if 'graph_default_start' not in st.session_state:
            st.session_state.graph_default_start = datetime.now().date() - timedelta(days=7)
        if 'graph_default_end' not in st.session_state:
            st.session_state.graph_default_end = datetime.now().date()
        if 'graph_last_quick_range' not in st.session_state:
            st.session_state.graph_last_quick_range = "Son 7 Gün"
        
        col1, col2, col3 = st.columns([2, 2, 1])
        
        with col3:
            graph_quick_range = st.selectbox(
                "Hızlı Seçim",
                ["Özel", "Bugün", "Dün", "Son 7 Gün", "Son 30 Gün", "Bu Ay"],
                index=["Özel", "Bugün", "Dün", "Son 7 Gün", "Son 30 Gün", "Bu Ay"].index(st.session_state.graph_last_quick_range) if st.session_state.graph_last_quick_range in ["Özel", "Bugün", "Dün", "Son 7 Gün", "Son 30 Gün", "Bu Ay"] else 3,
                key="graph_quick_input"
            )
            
            # Check if quick range changed
            if graph_quick_range != st.session_state.graph_last_quick_range and graph_quick_range != "Özel":
                st.session_state.graph_last_quick_range = graph_quick_range
                
                if graph_quick_range == "Bugün":
                    st.session_state.graph_default_start = datetime.now().date()
                    st.session_state.graph_default_end = datetime.now().date()
                elif graph_quick_range == "Dün":
                    yesterday = datetime.now().date() - timedelta(days=1)
                    st.session_state.graph_default_start = yesterday
                    st.session_state.graph_default_end = yesterday
                elif graph_quick_range == "Son 7 Gün":
                    st.session_state.graph_default_start = datetime.now().date() - timedelta(days=7)
                    st.session_state.graph_default_end = datetime.now().date()
                elif graph_quick_range == "Son 30 Gün":
                    st.session_state.graph_default_start = datetime.now().date() - timedelta(days=30)
                    st.session_state.graph_default_end = datetime.now().date()
                elif graph_quick_range == "Bu Ay":
                    st.session_state.graph_default_start = datetime.now().date().replace(day=1)
                    st.session_state.graph_default_end = datetime.now().date()
                
                st.rerun()
        
        with col1:
            graph_start_date = st.date_input(
                "Başlangıç",
                value=st.session_state.graph_default_start,
                max_value=datetime.now().date(),
                key="graph_start_input"
            )
            if graph_start_date != st.session_state.graph_default_start:
                st.session_state.graph_last_quick_range = "Özel"
        
        with col2:
            graph_end_date = st.date_input(
                "Bitiş",
                value=st.session_state.graph_default_end,
                max_value=datetime.now().date(),
                key="graph_end_input"
            )
            if graph_end_date != st.session_state.graph_default_end:
                st.session_state.graph_last_quick_range = "Özel"
        
        st.markdown("---")
        
        # Generate sales report for graphs
        graph_sales_report = generate_sales_report(db, graph_start_date, graph_end_date)
        
        if not graph_sales_report or not graph_sales_report['daily_data']:
            st.info(f"📊 {graph_start_date.strftime('%d.%m.%Y')} - {graph_end_date.strftime('%d.%m.%Y')} tarihleri arasında veri bulunamadı.")
        else:
            # Simple text-based charts since we don't have plotly
            st.info("🚧 Gelişmiş grafikler için plotly kütüphanesi gerekiyor. Şimdilik basit görselleştirmeler kullanılıyor.")
            
            # Revenue by day
            st.markdown("### 💰 Günlük Ciro Trendi")
            
            max_revenue = max([d['revenue'] for d in graph_sales_report['daily_data'].values()])
            for date, data in sorted(graph_sales_report['daily_data'].items()):
                bar_length = int(data['revenue'] / max_revenue * 50) if max_revenue > 0 else 0
                bar = "█" * bar_length
                st.text(f"{date.strftime('%d.%m')}: {bar} ₺{data['revenue']:.2f}")
            
            # Orders by day
            st.markdown("### 📊 Günlük Sipariş Sayısı")
            
            max_orders = max([d['orders'] for d in graph_sales_report['daily_data'].values()])
            for date, data in sorted(graph_sales_report['daily_data'].items()):
                bar_length = int(data['orders'] / max_orders * 50) if max_orders > 0 else 0
                bar = "▓" * bar_length
                st.text(f"{date.strftime('%d.%m')}: {bar} {data['orders']} sipariş")
    
    # Close database
    db.close()
    


if __name__ == "__main__":
    main()
