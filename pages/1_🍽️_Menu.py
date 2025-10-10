"""
Menu Page - Display and browse menu items
"""

import streamlit as st
from database.db_manager import get_db
from utils.session_manager import init_session_state, add_to_cart, get_cart_count
from utils.page_navigation import show_customer_navigation, hide_default_sidebar
import pandas as pd

# Get restaurant info for dynamic branding
db = get_db()
restaurant = db.get_restaurant_info()
db.close()

# Page config with dynamic title
st.set_page_config(
    page_title=f"Menü - {restaurant.name_tr}",
    page_icon="🍽️",
    layout="wide"
)

# Hide default sidebar
hide_default_sidebar()

# Initialize session
init_session_state()

# Show customer navigation
show_customer_navigation()

# Custom CSS
st.markdown("""
<style>
    .menu-item-card {
        border: 2px solid #f0f2f6;
        border-radius: 15px;
        padding: 1.5rem;
        margin: 1rem 0;
        background: white;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        transition: all 0.3s ease;
    }
    .menu-item-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 4px 12px rgba(0,0,0,0.15);
        border-color: #667eea;
    }
    .price-tag {
        font-size: 1.5rem;
        font-weight: bold;
        color: #667eea;
    }
    .category-badge {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 0.5rem 1rem;
        border-radius: 20px;
        display: inline-block;
        margin: 0.2rem;
    }
    .badge {
        padding: 0.3rem 0.8rem;
        border-radius: 12px;
        font-size: 0.85rem;
        margin: 0.2rem;
        display: inline-block;
    }
    .vegetarian { background-color: #d4edda; color: #155724; }
    .vegan { background-color: #c3e6cb; color: #0c5d2a; }
    .spicy { background-color: #f8d7da; color: #721c24; }
</style>
""", unsafe_allow_html=True)

def show_filters(db):
    """Display filter options"""
    st.sidebar.markdown("### 🔍 Filtreler")
    
    # Category filter
    categories = db.get_all_categories()
    category_names = ["Tümü"] + [cat.name for cat in categories]
    selected_category = st.sidebar.selectbox(
        "Kategori",
        category_names,
        key="category_filter"
    )
    
    # Dietary filters
    st.sidebar.markdown("#### 🌱 Beslenme Tercihleri")
    show_vegetarian = st.sidebar.checkbox("Vejetaryen", key="filter_veg")
    show_vegan = st.sidebar.checkbox("Vegan", key="filter_vegan")
    
    # Spicy filter
    st.sidebar.markdown("#### 🌶️ Acılık")
    spicy_only = st.sidebar.checkbox("Sadece Acılı", key="filter_spicy")
    
    # Price range
    st.sidebar.markdown("#### 💰 Fiyat Aralığı")
    price_range = st.sidebar.slider(
        "Maksimum Fiyat (TL)",
        0, 1000, 1000,
        key="price_slider"
    )
    
    # Search
    st.sidebar.markdown("#### 🔎 Arama")
    search_term = st.sidebar.text_input(
        "Ürün Ara",
        placeholder="Pizza, salata, vs...",
        key="search_input"
    )
    
    return {
        'category': selected_category,
        'vegetarian': show_vegetarian,
        'vegan': show_vegan,
        'spicy': spicy_only,
        'max_price': price_range,
        'search': search_term
    }

def filter_items(items, filters):
    """Apply filters to menu items"""
    filtered = items
    
    # Vegetarian filter
    if filters['vegetarian']:
        filtered = [item for item in filtered if item.is_vegetarian]
    
    # Vegan filter
    if filters['vegan']:
        filtered = [item for item in filtered if item.is_vegan]
    
    # Spicy filter
    if filters['spicy']:
        filtered = [item for item in filtered if item.is_spicy]
    
    # Price filter
    filtered = [item for item in filtered if item.price <= filters['max_price']]
    
    # Search filter
    if filters['search']:
        search_lower = filters['search'].lower()
        filtered = [
            item for item in filtered 
            if search_lower in item.name.lower() or 
               search_lower in (item.description or "").lower()
        ]
    
    return filtered

def display_menu_item(item, col):
    """Display a single menu item"""
    with col:
        # Item name and badges
        st.markdown(f"### {item.name}")
        
        badges_html = ""
        if item.is_vegetarian:
            badges_html += '<span class="badge vegetarian">🌱 Vejetaryen</span>'
        if item.is_vegan:
            badges_html += '<span class="badge vegan">🥬 Vegan</span>'
        if item.is_spicy:
            badges_html += f'<span class="badge spicy">🌶️ Acı {item.spicy_level}/5</span>'
        
        if badges_html:
            st.markdown(badges_html, unsafe_allow_html=True)
        
        # Description
        if item.description:
            st.markdown(f"*{item.description}*")
        
        # Ingredients
        if item.ingredients:
            with st.expander("📝 İçindekiler"):
                st.write(item.ingredients)
                if item.allergens:
                    st.warning(f"⚠️ Alerjenler: {item.allergens}")
        
        # Price and actions
        col1, col2 = st.columns([1, 2])
        
        with col1:
            st.markdown(f'<p class="price-tag">{item.price} ₺</p>', unsafe_allow_html=True)
        
        with col2:
            quantity = st.number_input(
                "Adet",
                min_value=1,
                max_value=10,
                value=1,
                key=f"qty_{item.id}",
                label_visibility="collapsed"
            )
            
            if st.button(f"🛒 Sepete Ekle", key=f"add_{item.id}", type="primary", use_container_width=True):
                add_to_cart(item.id, item.name, item.price, quantity)
                st.success(f"✅ {quantity}x {item.name} sepete eklendi!")
                st.rerun()
        
        # Additional info
        col_info1, col_info2 = st.columns(2)
        with col_info1:
            if item.calories:
                st.caption(f"🔥 {item.calories} kcal")
        with col_info2:
            if item.order_count > 0:
                st.caption(f"⭐ {item.order_count} sipariş")
        
        st.markdown("---")

def main():
    """Main menu page"""
    # Get restaurant info
    db_temp = get_db()
    restaurant = db_temp.get_restaurant_info()
    db_temp.close()
    
    # # Show header with restaurant branding
    # if restaurant.logo_url:
    #     col1, col2, col3 = st.columns([1, 2, 1])
    #     with col2:
    #         try:
    #             st.image(restaurant.logo_url, width=250)
    #         except:
    #             pass
    
    st.title(f"🍽️ {restaurant.name_tr} - Menümüz")
    
    if restaurant.about_tr:
        st.caption(restaurant.about_tr)
    
    st.markdown("---")
    
    # Get database connection
    db = get_db()
    
    # Show cart summary in sidebar
    cart_count = get_cart_count()
    if cart_count > 0:
        st.sidebar.success(f"🛒 Sepetinizde {cart_count} ürün var")
        if st.sidebar.button("📦 Sepete Git", type="primary"):
            st.switch_page("pages/2_🛒_Cart.py")
    
    # Show filters
    filters = show_filters(db)
    
    # Get categories
    categories = db.get_all_categories()
    
    # Get menu items
    if filters['category'] == "Tümü":
        items = db.get_all_menu_items()
    else:
        # Find category ID
        category = next((cat for cat in categories if cat.name == filters['category']), None)
        if category:
            items = db.get_menu_items_by_category(category.id)
        else:
            items = []
    
    # Apply filters
    filtered_items = filter_items(items, filters)
    
    # Display results
    if not filtered_items:
        st.warning("⚠️ Filtre kriterlerinize uygun ürün bulunamadı. Lütfen filtreleri değiştirin.")
        db.close()
        return
    
    st.info(f"📊 {len(filtered_items)} ürün gösteriliyor")
    
    # Group by category for better organization
    items_by_category = {}
    for item in filtered_items:
        cat_name = next((cat.name for cat in categories if cat.id == item.category_id), "Diğer")
        if cat_name not in items_by_category:
            items_by_category[cat_name] = []
        items_by_category[cat_name].append(item)
    
    # Display items by category
    for cat_name, cat_items in items_by_category.items():
        category = next((cat for cat in categories if cat.name == cat_name), None)
        icon = category.icon if category else "📁"
        
        st.markdown(f'<div class="category-badge">{icon} {cat_name} ({len(cat_items)})</div>', 
                   unsafe_allow_html=True)
        st.markdown("")
        
        # Display items in 2 columns
        cols = st.columns(2)
        for idx, item in enumerate(cat_items):
            display_menu_item(item, cols[idx % 2])
    
    # Close database connection
    db.close()
    
    # Quick actions
    st.markdown("---")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("🏠 Ana Sayfa", use_container_width=True):
            st.switch_page("app.py")
    
    with col2:
        if st.button("🤖 AI Asistan", use_container_width=True):
            st.switch_page("pages/3_💬_AI_Assistant.py")
    
    with col3:
        if st.button("🛒 Sepet", use_container_width=True):
            st.switch_page("pages/2_🛒_Cart.py")

if __name__ == "__main__":
    main()
