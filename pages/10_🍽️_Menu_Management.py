"""
Menu Management Page - Manage menu items with CRUD operations
Admin only access - requires authentication
"""

import streamlit as st
from database.db_manager import get_db
from database.models import MenuItem
from utils.session_manager import init_session_state
from utils.page_navigation import show_admin_navigation, hide_default_sidebar
from datetime import datetime

# Page config
st.set_page_config(page_title="Menü Yönetimi", page_icon="🍽️", layout="wide")

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
    .product-card {
        background: white;
        border: 2px solid #f0f2f6;
        border-radius: 10px;
        padding: 1rem;
        margin: 0.5rem 0;
    }
    .product-available {
        border-color: #28a745;
        background: #f0fff4;
    }
    .product-unavailable {
        border-color: #dc3545;
        background: #fff5f5;
    }
</style>
""", unsafe_allow_html=True)

def main():
    """Main menu management page"""
    st.title("🍽️ Menü Yönetimi")
    
    # Get database
    db = get_db()
    
    # Quick stats
    all_items = db.get_all_menu_items(available_only=False)
    available_items = [i for i in all_items if i.is_available]
    categories = db.get_all_categories()
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("📊 Toplam Ürün", len(all_items))
    with col2:
        st.metric("✅ Mevcut Ürün", len(available_items))
    with col3:
        st.metric("📂 Kategori", len(categories))
    
    st.markdown("---")
    
    # Main tabs
    tab1, tab2, tab3, tab4 = st.tabs(["📋 Ürün Listesi", "➕ Yeni Ürün", "✏️ Düzenle", "🗑️ Sil"])
    
    with tab1:
        # Product list with quick actions
        st.markdown("### 📋 Ürün Listesi")
        
        categories = db.get_all_categories()
        
        for category in categories:
            with st.expander(f"{category.icon} {category.name}", expanded=False):
                items = db.get_menu_items_by_category(category.id, available_only=False)
                
                if not items:
                    st.info("Bu kategoride ürün yok.")
                    continue
                
                for item in items:
                    col1, col2, col3, col4, col5 = st.columns([3, 1, 1, 1, 1])
                    
                    with col1:
                        st.write(f"**{item.name}**")
                        st.caption(item.description[:50] + "..." if item.description else "")
                    
                    with col2:
                        st.write(f"**{item.price} ₺**")
                    
                    with col3:
                        # Quick price update
                        new_price = st.number_input(
                            "Fiyat",
                            min_value=0.0,
                            value=float(item.price),
                            step=5.0,
                            key=f"price_{item.id}",
                            label_visibility="collapsed"
                        )
                        if new_price != item.price:
                            if st.button("💾", key=f"save_price_{item.id}"):
                                db.update_menu_item(item.id, price=new_price)
                                st.success("Güncellendi!")
                                st.rerun()
                    
                    with col4:
                        availability = "✅" if item.is_available else "❌"
                        new_status = st.checkbox(
                            availability,
                            value=item.is_available,
                            key=f"avail_{item.id}",
                            label_visibility="collapsed"
                        )
                        
                        if new_status != item.is_available:
                            db.update_menu_item(item.id, is_available=new_status)
                            st.rerun()
                    
                    with col5:
                        if st.button("🗑️", key=f"del_{item.id}", help="Sil"):
                            if st.session_state.get(f'confirm_delete_{item.id}'):
                                # Delete the item
                                try:
                                    # Get item ID before deleting
                                    item_id = item.id
                                    item_name = item.name
                                    
                                    # Re-fetch from session to avoid detached instance
                                    fresh_item = db.session.query(MenuItem).get(item_id)
                                    if fresh_item:
                                        db.session.delete(fresh_item)
                                        db.session.commit()
                                        
                                        # Clear confirmation state
                                        if f'confirm_delete_{item_id}' in st.session_state:
                                            del st.session_state[f'confirm_delete_{item_id}']
                                        
                                        st.success(f"{item_name} silindi!")
                                        st.rerun()
                                except Exception as e:
                                    st.error(f"Silme hatası: {str(e)}")
                            else:
                                st.session_state[f'confirm_delete_{item.id}'] = True
                                st.warning("Tekrar tıklayarak onaylayın")
    
    with tab2:
        # Add new product
        st.markdown("### ➕ Yeni Ürün Ekle")
        
        with st.form("add_product_form"):
            col1, col2 = st.columns(2)
            
            with col1:
                categories = db.get_all_categories()
                category_id = st.selectbox(
                    "Kategori *",
                    [(cat.id, cat.name) for cat in categories],
                    format_func=lambda x: x[1]
                )[0]
                
                name = st.text_input("Ürün Adı (TR) *", placeholder="Margarita Pizza")
                name_en = st.text_input("Ürün Adı (EN)", placeholder="Margherita Pizza")
                
                description = st.text_area(
                    "Açıklama (TR) *",
                    placeholder="Domates sos, mozzarella, fesleğen"
                )
                description_en = st.text_area(
                    "Açıklama (EN)",
                    placeholder="Tomato sauce, mozzarella, basil"
                )
                
                price = st.number_input("Fiyat (₺) *", min_value=0.0, value=85.0, step=5.0)
                calories = st.number_input("Kalori", min_value=0, value=0, step=50)
            
            with col2:
                st.markdown("#### Özellikler")
                is_vegetarian = st.checkbox("🌱 Vejetaryen")
                is_vegan = st.checkbox("🥬 Vegan")
                is_spicy = st.checkbox("🌶️ Acılı")
                
                spicy_level = 0
                if is_spicy:
                    spicy_level = st.slider("Acılık Seviyesi", 1, 5, 2)
                
                st.markdown("#### Alerjen ve İçerik")
                allergens = st.text_input(
                    "Alerjenler",
                    placeholder="gluten, dairy",
                    help="Virgülle ayırın"
                )
                
                ingredients = st.text_input(
                    "İçindekiler",
                    placeholder="hamur, domates, peynir, fesleğen"
                )
            
            st.markdown("#### 🖼️ Görsel")
            
            col_img1, col_img2 = st.columns(2)
            
            with col_img1:
                image_file = st.file_uploader(
                    "Görsel Yükle",
                    type=['png', 'jpg', 'jpeg', 'webp'],
                    help="Ürün görseli yükleyin (PNG, JPG, JPEG, WEBP)",
                    key="add_product_image"
                )
            
            with col_img2:
                image_url_input = st.text_input(
                    "veya URL Girin",
                    placeholder="https://...",
                    help="Görsel URL'si (upload etmiyorsanız)"
                )
            
            submitted = st.form_submit_button("➕ Ürün Ekle", type="primary", use_container_width=True)
            
            if submitted:
                if not name or not description or price <= 0:
                    st.error("⚠️ Lütfen gerekli alanları doldurun!")
                else:
                    try:
                        # Handle image upload
                        image_url = image_url_input  # Default to URL input
                        
                        if image_file is not None:
                            # Save uploaded file
                            import os
                            from datetime import datetime
                            
                            # Create uploads directory if not exists
                            upload_dir = "static/images/products"
                            os.makedirs(upload_dir, exist_ok=True)
                            
                            # Generate unique filename
                            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                            file_extension = image_file.name.split('.')[-1]
                            filename = f"product_{timestamp}.{file_extension}"
                            filepath = os.path.join(upload_dir, filename)
                            
                            # Save file
                            with open(filepath, 'wb') as f:
                                f.write(image_file.getbuffer())
                            
                            image_url = filepath
                            st.success(f"📸 Görsel yüklendi: {filename}")
                        
                        new_item = db.create_menu_item(
                            category_id=category_id,
                            name=name,
                            name_en=name_en or name,
                            description=description,
                            description_en=description_en or description,
                            price=price,
                            is_vegetarian=is_vegetarian,
                            is_vegan=is_vegan,
                            is_spicy=is_spicy,
                            spicy_level=spicy_level,
                            allergens=allergens,
                            ingredients=ingredients,
                            calories=calories if calories > 0 else None,
                            image_url=image_url or None
                        )
                        st.success(f"✅ {name} başarıyla eklendi!")
                        st.balloons()
                        
                        # Rebuild vector index
                        st.info("🔄 AI vektör veritabanı güncelleniyor...")
                        from ai.rag_engine import get_rag_engine
                        try:
                            engine = get_rag_engine()
                            engine.rebuild_index()
                            st.success("✅ AI veritabanı güncellendi!")
                        except Exception as e:
                            st.warning(f"AI güncelleme hatası: {e}")
                        
                        st.rerun()
                    except Exception as e:
                        st.error(f"Hata: {e}")
    
    with tab3:
        # Edit existing product
        st.markdown("### ✏️ Ürün Düzenle")
        
        # Select product to edit
        all_items = db.get_all_menu_items(available_only=False)
        
        if not all_items:
            st.info("Henüz ürün yok.")
        else:
            # Add empty option to allow deselection
            item_options = ["-- Ürün Seçin --"] + [f"{item.name} ({item.price} ₺)" for item in all_items]
            
            selected_index = st.selectbox(
                "Düzenlenecek Ürünü Seçin",
                range(len(item_options)),
                format_func=lambda x: item_options[x]
            )
            
            # Get selected item (skip first index which is empty)
            selected_item = all_items[selected_index - 1] if selected_index > 0 else None
            
            if selected_item:
                st.markdown(f"#### {selected_item.name} Düzenleniyor")
                
                with st.form("edit_product_form"):
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        categories = db.get_all_categories()
                        category_id = st.selectbox(
                            "Kategori",
                            [(cat.id, cat.name) for cat in categories],
                            index=next((i for i, cat in enumerate(categories) if cat.id == selected_item.category_id), 0),
                            format_func=lambda x: x[1]
                        )[0]
                        
                        name = st.text_input("Ürün Adı (TR)", value=selected_item.name)
                        name_en = st.text_input("Ürün Adı (EN)", value=selected_item.name_en or "")
                        
                        description = st.text_area("Açıklama (TR)", value=selected_item.description or "")
                        description_en = st.text_area("Açıklama (EN)", value=selected_item.description_en or "")
                        
                        price = st.number_input("Fiyat (₺)", min_value=0.0, value=float(selected_item.price), step=5.0)
                        calories = st.number_input("Kalori", min_value=0, value=selected_item.calories or 0, step=50)
                    
                    with col2:
                        st.markdown("#### Özellikler")
                        is_vegetarian = st.checkbox("🌱 Vejetaryen", value=selected_item.is_vegetarian)
                        is_vegan = st.checkbox("🥬 Vegan", value=selected_item.is_vegan)
                        is_spicy = st.checkbox("🌶️ Acılı", value=selected_item.is_spicy)
                        
                        spicy_level = st.slider("Acılık Seviyesi", 0, 5, selected_item.spicy_level)
                        
                        is_available = st.checkbox("✅ Mevcut", value=selected_item.is_available)
                        
                        st.markdown("#### Alerjen ve İçerik")
                        allergens = st.text_input("Alerjenler", value=selected_item.allergens or "")
                        ingredients = st.text_input("İçindekiler", value=selected_item.ingredients or "")
                        
                        st.markdown("#### Görsel Yönetimi")
                        
                        # Show current image if exists
                        if selected_item.image_url:
                            st.markdown("**Mevcut Görsel:**")
                            try:
                                col_prev1, col_prev2 = st.columns([1, 2])
                                with col_prev1:
                                    st.image(selected_item.image_url, width=120)
                                with col_prev2:
                                    st.caption(f"📁 {selected_item.image_url}")
                                    delete_image = st.checkbox("🗑️ Görseli Sil", key="delete_image")
                            except:
                                st.caption(f"📁 {selected_item.image_url}")
                                delete_image = st.checkbox("🗑️ Görseli Sil", key="delete_image")
                        else:
                            delete_image = False
                        
                        # Upload new image or URL
                        col_img1, col_img2 = st.columns(2)
                        with col_img1:
                            image_file = st.file_uploader("Yeni Görsel Yükle", type=['png', 'jpg', 'jpeg', 'webp'], key="edit_image_file", help="PNG, JPG, JPEG veya WEBP formatında görsel yükleyebilirsiniz")
                        with col_img2:
                            image_url_input = st.text_input("veya Görsel URL", value="" if delete_image else (selected_item.image_url or ""), key="edit_image_url", help="Dış kaynaklı görsel URL'si girebilirsiniz")
                    
                    submitted = st.form_submit_button("💾 Güncelle", type="primary", use_container_width=True)
                    
                    if submitted:
                        try:
                            # Handle image upload/update
                            image_url = None
                            
                            if delete_image:
                                # User wants to delete image
                                image_url = None
                            elif image_file is not None:
                                # Upload new image
                                import os
                                from datetime import datetime
                                
                                # Create uploads directory if not exists
                                upload_dir = "static/images/products"
                                os.makedirs(upload_dir, exist_ok=True)
                                
                                # Generate unique filename
                                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                                file_extension = image_file.name.split('.')[-1]
                                filename = f"product_{timestamp}.{file_extension}"
                                filepath = os.path.join(upload_dir, filename)
                                
                                # Save file
                                with open(filepath, 'wb') as f:
                                    f.write(image_file.getbuffer())
                                
                                image_url = filepath
                                st.success(f"📸 Yeni görsel yüklendi: {filename}")
                                
                                # Delete old image file if it was uploaded (not a URL)
                                if selected_item.image_url and selected_item.image_url.startswith("static/"):
                                    try:
                                        if os.path.exists(selected_item.image_url):
                                            os.remove(selected_item.image_url)
                                    except:
                                        pass
                            elif image_url_input:
                                # Use URL
                                image_url = image_url_input
                            else:
                                # Keep existing if nothing changed
                                image_url = selected_item.image_url
                            
                            db.update_menu_item(
                                selected_item.id,
                                category_id=category_id,
                                name=name,
                                name_en=name_en,
                                description=description,
                                description_en=description_en,
                                price=price,
                                is_vegetarian=is_vegetarian,
                                is_vegan=is_vegan,
                                is_spicy=is_spicy,
                                spicy_level=spicy_level,
                                allergens=allergens,
                                ingredients=ingredients,
                                calories=calories if calories > 0 else None,
                                image_url=image_url,
                                is_available=is_available
                            )
                            st.success("✅ Ürün güncellendi!")
                            
                            # Rebuild vector index
                            st.info("🔄 AI vektör veritabanı güncelleniyor...")
                            from ai.rag_engine import get_rag_engine
                            try:
                                engine = get_rag_engine()
                                engine.rebuild_index()
                                st.success("✅ AI veritabanı güncellendi!")
                            except:
                                pass
                            
                            st.rerun()
                        except Exception as e:
                            st.error(f"Hata: {e}")
    
    with tab4:
        # Delete products (bulk)
        st.markdown("### 🗑️ Ürün Sil")
        st.warning("⚠️ Silme işlemi geri alınamaz!")
        
        categories = db.get_all_categories()
        selected_category = st.selectbox(
            "Kategori Seçin",
            [None] + categories,
            format_func=lambda x: "Tüm Kategoriler" if x is None else f"{x.icon} {x.name}"
        )
        
        if selected_category:
            items = db.get_menu_items_by_category(selected_category.id, available_only=False)
        else:
            items = db.get_all_menu_items(available_only=False)
        
        if items:
            st.markdown(f"**{len(items)} ürün bulundu**")
            
            selected_items = st.multiselect(
                "Silinecek Ürünleri Seçin",
                items,
                format_func=lambda x: f"{x.name} ({x.price} ₺)"
            )
            
            if selected_items:
                col1, col2 = st.columns(2)
                
                with col1:
                    st.warning(f"⚠️ {len(selected_items)} ürün silinecek!")
                
                with col2:
                    if st.button("🗑️ Seçilenleri Sil", type="primary", use_container_width=True):
                        try:
                            # Get item IDs first to avoid session issues
                            item_ids = [item.id for item in selected_items]
                            
                            for item_id in item_ids:
                                # Re-fetch item from session
                                item = db.session.query(MenuItem).get(item_id)
                                if item:
                                    db.session.delete(item)
                            
                            db.session.commit()
                            st.success(f"✅ {len(item_ids)} ürün silindi!")
                            
                            # Rebuild vector index
                            from ai.rag_engine import get_rag_engine
                            try:
                                engine = get_rag_engine()
                                engine.rebuild_index()
                            except:
                                pass
                            
                            st.rerun()
                        except Exception as e:
                            st.error(f"Hata: {e}")
                            db.session.rollback()
        else:
            st.info("Bu kategoride ürün yok.")
    
    # Close database
    db.close()

if __name__ == "__main__":
    main()
