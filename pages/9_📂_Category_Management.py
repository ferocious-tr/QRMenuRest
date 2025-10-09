"""
Category Management - Manage menu categories
Admin only access - requires authentication through admin.py
"""

import streamlit as st
from database.db_manager import get_db
from database.models import Category
from utils.session_manager import init_session_state
from utils.page_navigation import show_admin_navigation, hide_default_sidebar
from datetime import datetime
from ai.rag_engine import MenuRAGEngine

# Page config
st.set_page_config(page_title="Kategori Yönetimi", page_icon="📂", layout="wide")

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
    .category-card {
        background: white;
        border-radius: 12px;
        padding: 1.5rem;
        margin: 0.5rem 0;
        box-shadow: 0 2px 6px rgba(0,0,0,0.08);
        border-left: 4px solid #667eea;
    }
    .category-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
    }
    .category-name {
        font-size: 1.5rem;
        font-weight: bold;
        color: #2d3748;
    }
    .category-count {
        background: #667eea;
        color: white;
        padding: 0.3rem 0.8rem;
        border-radius: 20px;
        font-size: 0.9rem;
        font-weight: bold;
    }
    .stat-box {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border-radius: 15px;
        padding: 1.5rem;
        text-align: center;
    }
    .stat-value {
        font-size: 2rem;
        font-weight: bold;
    }
    .stat-label {
        font-size: 0.9rem;
        opacity: 0.9;
        margin-top: 0.5rem;
    }
</style>
""", unsafe_allow_html=True)

def get_category_stats(db, category_id):
    """Get statistics for a category"""
    from sqlalchemy import func
    from database.models import MenuItem, OrderItem
    
    # Count items
    item_count = db.session.query(func.count(MenuItem.id)).filter(
        MenuItem.category_id == category_id
    ).scalar()
    
    # Count active items
    active_count = db.session.query(func.count(MenuItem.id)).filter(
        MenuItem.category_id == category_id,
        MenuItem.is_available == True
    ).scalar()
    
    # Calculate total revenue from this category
    total_revenue = db.session.query(
        func.sum(OrderItem.subtotal)
    ).join(
        MenuItem, OrderItem.menu_item_id == MenuItem.id
    ).filter(
        MenuItem.category_id == category_id
    ).scalar() or 0
    
    # Count total orders
    order_count = db.session.query(
        func.count(OrderItem.id.distinct())
    ).join(
        MenuItem, OrderItem.menu_item_id == MenuItem.id
    ).filter(
        MenuItem.category_id == category_id
    ).scalar() or 0
    
    return {
        'item_count': item_count,
        'active_count': active_count,
        'total_revenue': float(total_revenue),
        'order_count': order_count
    }

def rebuild_vector_db():
    """Rebuild vector database after category changes"""
    try:
        rag_engine = MenuRAGEngine()
        rag_engine.rebuild_index()
        return True
    except Exception as e:
        st.error(f"Vector DB yeniden oluşturulurken hata: {e}")
        return False

def main():
    """Main category management page"""
    st.title("📂 Kategori Yönetimi")
    
    # Quick stats at top
    db = get_db()
    all_categories = db.get_all_categories()
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown(f"""
        <div class="stat-box">
            <div class="stat-value">{len(all_categories)}</div>
            <div class="stat-label">📂 Toplam Kategori</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        total_items = sum(len(db.get_menu_items_by_category(c.id)) for c in all_categories)
        st.markdown(f"""
        <div class="stat-box">
            <div class="stat-value">{total_items}</div>
            <div class="stat-label">🍽️ Toplam Ürün</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        active_categories = len([c for c in all_categories if any(
            item.is_available for item in db.get_menu_items_by_category(c.id)
        )])
        st.markdown(f"""
        <div class="stat-box">
            <div class="stat-value">{active_categories}</div>
            <div class="stat-label">✅ Aktif Kategori</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        empty_categories = len([c for c in all_categories if len(db.get_menu_items_by_category(c.id)) == 0])
        st.markdown(f"""
        <div class="stat-box">
            <div class="stat-value">{empty_categories}</div>
            <div class="stat-label">📭 Boş Kategori</div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Main tabs
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "📋 Kategori Listesi",
        "➕ Yeni Kategori",
        "✏️ Düzenle",
        "🗑️ Sil",
        "📊 İstatistikler"
    ])
    
    with tab1:
        st.markdown("## 📋 Tüm Kategoriler")
        
        if not all_categories:
            st.info("📭 Henüz kategori eklenmemiş.")
        else:
            # Display order selector
            col1, col2 = st.columns([3, 1])
            with col2:
                sort_by = st.selectbox(
                    "Sıralama",
                    ["Sıra Numarası", "İsim (A-Z)", "İsim (Z-A)", "Ürün Sayısı"],
                    key="sort_categories"
                )
            
            # Sort categories
            if sort_by == "Sıra Numarası":
                sorted_categories = sorted(all_categories, key=lambda x: x.display_order)
            elif sort_by == "İsim (A-Z)":
                sorted_categories = sorted(all_categories, key=lambda x: x.name)
            elif sort_by == "İsim (Z-A)":
                sorted_categories = sorted(all_categories, key=lambda x: x.name, reverse=True)
            else:  # Ürün Sayısı
                sorted_categories = sorted(
                    all_categories, 
                    key=lambda x: len(db.get_menu_items_by_category(x.id)),
                    reverse=True
                )
            
            # Display categories
            for category in sorted_categories:
                items = db.get_menu_items_by_category(category.id)
                stats = get_category_stats(db, category.id)
                
                with st.container():
                    col1, col2, col3 = st.columns([3, 2, 1])
                    
                    with col1:
                        st.markdown(f"### {category.icon} {category.name}")
                        if category.description:
                            st.caption(category.description)
                    
                    with col2:
                        st.metric("Ürün Sayısı", stats['item_count'])
                        st.caption(f"✅ {stats['active_count']} aktif")
                    
                    with col3:
                        # Quick edit display order
                        new_order = st.number_input(
                            "Sıra",
                            min_value=0,
                            max_value=100,
                            value=category.display_order,
                            key=f"order_{category.id}"
                        )
                        
                        if new_order != category.display_order:
                            category.display_order = new_order
                            db.session.commit()
                            st.success("✅ Sıra güncellendi")
                            st.rerun()
                    
                    # Show items in category
                    if items:
                        with st.expander(f"📦 Ürünleri Görüntüle ({len(items)} adet)"):
                            for item in items:
                                status = "✅" if item.is_available else "❌"
                                st.write(f"{status} {item.name} - ₺{item.price}")
                    
                    st.markdown("---")
    
    with tab2:
        st.markdown("## ➕ Yeni Kategori Ekle")
        
        with st.form("add_category_form"):
            col1, col2 = st.columns(2)
            
            with col1:
                new_name = st.text_input(
                    "Kategori Adı *",
                    placeholder="Örn: Başlangıçlar",
                    help="Türkçe kategori adı"
                )
                
                new_icon = st.text_input(
                    "İkon",
                    value="🍽️",
                    placeholder="🍽️",
                    help="Kategoriyi temsil eden emoji"
                )
                
                new_description = st.text_area(
                    "Açıklama",
                    placeholder="Kategori hakkında kısa açıklama...",
                    height=100
                )
            
            with col2:
                new_name_en = st.text_input(
                    "Kategori Adı (İngilizce)",
                    placeholder="Örn: Appetizers",
                    help="İngilizce kategori adı (opsiyonel)"
                )
                
                new_order = st.number_input(
                    "Sıra Numarası",
                    min_value=0,
                    max_value=100,
                    value=len(all_categories) + 1,
                    help="Menüde görünme sırası"
                )
                
                new_is_active = st.checkbox(
                    "Aktif",
                    value=True,
                    help="Kategoriyi menüde göster"
                )
            
            submitted = st.form_submit_button("💾 Kategori Ekle", type="primary", use_container_width=True)
            
            if submitted:
                if not new_name:
                    st.error("❌ Kategori adı zorunludur!")
                else:
                    # Check duplicate
                    existing = db.session.query(Category).filter_by(name=new_name).first()
                    if existing:
                        st.error(f"❌ '{new_name}' adında bir kategori zaten var!")
                    else:
                        try:
                            # Create category
                            new_category = Category(
                                name=new_name,
                                name_en=new_name_en if new_name_en else new_name,
                                icon=new_icon,
                                description=new_description,
                                display_order=new_order,
                                is_active=new_is_active
                            )
                            
                            db.session.add(new_category)
                            db.session.commit()
                            
                            st.success(f"✅ '{new_name}' kategorisi başarıyla eklendi!")
                            st.balloons()
                            
                            # Rebuild vector DB
                            with st.spinner("Vector DB güncelleniyor..."):
                                rebuild_vector_db()
                            
                            st.rerun()
                            
                        except Exception as e:
                            st.error(f"❌ Kategori eklenirken hata: {e}")
                            db.session.rollback()
    
    with tab3:
        st.markdown("## ✏️ Kategori Düzenle")
        
        if not all_categories:
            st.info("Düzenlenecek kategori yok.")
        else:
            # Select category to edit
            category_options = {f"{c.icon} {c.name}": c.id for c in all_categories}
            selected_name = st.selectbox(
                "Düzenlenecek Kategoriyi Seçin",
                options=list(category_options.keys())
            )
            
            if selected_name:
                category_id = category_options[selected_name]
                category = db.session.query(Category).get(category_id)
                
                if category:
                    st.markdown("---")
                    
                    with st.form("edit_category_form"):
                        col1, col2 = st.columns(2)
                        
                        with col1:
                            edit_name = st.text_input(
                                "Kategori Adı *",
                                value=category.name
                            )
                            
                            edit_icon = st.text_input(
                                "İkon",
                                value=category.icon or "🍽️"
                            )
                            
                            edit_description = st.text_area(
                                "Açıklama",
                                value=category.description or "",
                                height=100
                            )
                        
                        with col2:
                            edit_name_en = st.text_input(
                                "Kategori Adı (İngilizce)",
                                value=category.name_en or category.name
                            )
                            
                            edit_order = st.number_input(
                                "Sıra Numarası",
                                min_value=0,
                                max_value=100,
                                value=category.display_order
                            )
                            
                            edit_is_active = st.checkbox(
                                "Aktif",
                                value=category.is_active if hasattr(category, 'is_active') else True
                            )
                        
                        # Show current stats
                        stats = get_category_stats(db, category.id)
                        st.info(f"📊 Bu kategoride **{stats['item_count']}** ürün var (✅ {stats['active_count']} aktif)")
                        
                        col_a, col_b = st.columns(2)
                        
                        with col_a:
                            update_btn = st.form_submit_button(
                                "💾 Güncelle",
                                type="primary",
                                use_container_width=True
                            )
                        
                        with col_b:
                            cancel_btn = st.form_submit_button(
                                "❌ İptal",
                                use_container_width=True
                            )
                        
                        if update_btn:
                            if not edit_name:
                                st.error("❌ Kategori adı zorunludur!")
                            else:
                                # Check duplicate (exclude current category)
                                existing = db.session.query(Category).filter(
                                    Category.name == edit_name,
                                    Category.id != category_id
                                ).first()
                                
                                if existing:
                                    st.error(f"❌ '{edit_name}' adında başka bir kategori var!")
                                else:
                                    try:
                                        # Update category
                                        category.name = edit_name
                                        category.name_en = edit_name_en
                                        category.icon = edit_icon
                                        category.description = edit_description
                                        category.display_order = edit_order
                                        if hasattr(category, 'is_active'):
                                            category.is_active = edit_is_active
                                        
                                        db.session.commit()
                                        
                                        st.success(f"✅ '{edit_name}' kategorisi güncellendi!")
                                        
                                        # Rebuild vector DB
                                        with st.spinner("Vector DB güncelleniyor..."):
                                            rebuild_vector_db()
                                        
                                        st.rerun()
                                        
                                    except Exception as e:
                                        st.error(f"❌ Güncelleme hatası: {e}")
                                        db.session.rollback()
    
    with tab4:
        st.markdown("## 🗑️ Kategori Sil")
        
        if not all_categories:
            st.info("Silinecek kategori yok.")
        else:
            st.warning("⚠️ **DİKKAT**: Kategori silme işlemi geri alınamaz!")
            
            # Show categories with item counts
            st.markdown("### Kategoriler")
            
            deletable_categories = []
            non_deletable_categories = []
            
            for category in all_categories:
                items = db.get_menu_items_by_category(category.id)
                if len(items) == 0:
                    deletable_categories.append(category)
                else:
                    non_deletable_categories.append(category)
            
            # Show non-deletable categories (with items)
            if non_deletable_categories:
                st.markdown("#### ⚠️ Silinemeyen Kategoriler (Ürün İçeren)")
                for category in non_deletable_categories:
                    items = db.get_menu_items_by_category(category.id)
                    st.warning(
                        f"🔒 **{category.icon} {category.name}** - "
                        f"{len(items)} ürün içeriyor. Önce ürünleri silmelisiniz."
                    )
            
            # Show deletable categories (empty)
            if deletable_categories:
                st.markdown("---")
                st.markdown("#### ✅ Silinebilir Kategoriler (Boş)")
                
                selected_to_delete = st.multiselect(
                    "Silinecek Kategorileri Seçin",
                    options=[f"{c.icon} {c.name}" for c in deletable_categories],
                    help="Sadece boş kategoriler silinebilir"
                )
                
                if selected_to_delete:
                    st.error(f"⚠️ **{len(selected_to_delete)}** kategori silinecek!")
                    
                    confirm_text = st.text_input(
                        "Onaylamak için 'SİL' yazın",
                        key="delete_confirm"
                    )
                    
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        if st.button("🗑️ Seçilenleri Sil", type="primary", use_container_width=True):
                            if confirm_text == "SİL":
                                try:
                                    deleted_count = 0
                                    
                                    for cat_name in selected_to_delete:
                                        # Find category
                                        category = next(
                                            (c for c in deletable_categories if f"{c.icon} {c.name}" == cat_name),
                                            None
                                        )
                                        
                                        if category:
                                            db.session.delete(category)
                                            deleted_count += 1
                                    
                                    db.session.commit()
                                    
                                    st.success(f"✅ {deleted_count} kategori silindi!")
                                    
                                    # Rebuild vector DB
                                    with st.spinner("Vector DB güncelleniyor..."):
                                        rebuild_vector_db()
                                    
                                    st.rerun()
                                    
                                except Exception as e:
                                    st.error(f"❌ Silme hatası: {e}")
                                    db.session.rollback()
                            else:
                                st.error("❌ Onay metni hatalı! 'SİL' yazmalısınız.")
                    
                    with col2:
                        if st.button("❌ İptal", use_container_width=True):
                            st.rerun()
            else:
                st.info("📭 Silinebilir boş kategori yok.")
    
    with tab5:
        st.markdown("## 📊 Kategori İstatistikleri")
        
        if not all_categories:
            st.info("İstatistik gösterilecek kategori yok.")
        else:
            # Prepare data
            category_data = []
            
            for category in all_categories:
                stats = get_category_stats(db, category.id)
                category_data.append({
                    'Kategori': f"{category.icon} {category.name}",
                    'Ürün Sayısı': stats['item_count'],
                    'Aktif Ürün': stats['active_count'],
                    'Toplam Ciro': f"₺{stats['total_revenue']:.2f}",
                    'Sipariş Sayısı': stats['order_count'],
                    'Sıra': category.display_order
                })
            
            # Display as dataframe
            import pandas as pd
            df = pd.DataFrame(category_data)
            
            st.dataframe(
                df.sort_values('Sıra'),
                use_container_width=True,
                hide_index=True
            )
            
            st.markdown("---")
            
            # Top performing categories
            st.markdown("### 🏆 En Başarılı Kategoriler")
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("#### 💰 Ciro Bazında")
                sorted_by_revenue = sorted(
                    [(c, get_category_stats(db, c.id)) for c in all_categories],
                    key=lambda x: x[1]['total_revenue'],
                    reverse=True
                )[:5]
                
                for i, (cat, stats) in enumerate(sorted_by_revenue, 1):
                    st.write(f"{i}. {cat.icon} **{cat.name}** - ₺{stats['total_revenue']:.2f}")
            
            with col2:
                st.markdown("#### 📦 Sipariş Sayısı Bazında")
                sorted_by_orders = sorted(
                    [(c, get_category_stats(db, c.id)) for c in all_categories],
                    key=lambda x: x[1]['order_count'],
                    reverse=True
                )[:5]
                
                for i, (cat, stats) in enumerate(sorted_by_orders, 1):
                    st.write(f"{i}. {cat.icon} **{cat.name}** - {stats['order_count']} sipariş")
            
            st.markdown("---")
            
            # Category distribution chart (ASCII)
            st.markdown("### 📊 Ürün Dağılımı")
            
            max_items = max(stats['item_count'] for _, stats in sorted_by_revenue)
            
            for category in sorted(all_categories, key=lambda x: x.display_order):
                stats = get_category_stats(db, category.id)
                bar_length = int((stats['item_count'] / max_items) * 40) if max_items > 0 else 0
                bar = "█" * bar_length
                st.text(f"{category.icon} {category.name:20} {bar} {stats['item_count']} ürün")
    
    # Close database
    db.close()
    
    # Navigation buttons
    st.markdown("---")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("⬅️ Dashboard'a Dön", use_container_width=True):
            st.switch_page("pages/1_📊_Dashboard.py")
    
    with col2:
        if st.button("🍽️ Menü Yönetimi", use_container_width=True):
            st.switch_page("pages/1_📊_Dashboard.py")
    
    with col3:
        if st.button("🏓 Masa Yönetimi", use_container_width=True):
            st.switch_page("pages/2_🏓_Table_Management.py")

if __name__ == "__main__":
    main()
