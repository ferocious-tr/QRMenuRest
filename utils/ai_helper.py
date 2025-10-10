"""
AI Helper Functions
Helper functions for AI assistant to interact with menu and cart
"""

import re
import streamlit as st
from database.db_manager import get_db


def extract_product_ids_from_response(response):
    """
    Extract product IDs from AI response
    Format: [PRODUCT:123] or [PRODUCT:name]
    """
    pattern = r'\[PRODUCT:(\d+)\]'
    matches = re.findall(pattern, response)
    return [int(pid) for pid in matches]


def format_product_for_chat(product_id, product_name, price, category, language='tr'):
    """
    Format product information for chat display with action buttons
    Returns formatted markdown with product ID embedded
    """
    if language == 'tr':
        return f"""
**{product_name}**
📁 {category} | 💰 {price} TL
[PRODUCT:{product_id}]
"""
    else:
        return f"""
**{product_name}**
📁 {category} | 💰 {price} TL
[PRODUCT:{product_id}]
"""


def create_product_card(product, key_suffix='', language='tr'):
    """
    Create an interactive product card for AI recommendations
    Returns a streamlit container with product info and add to cart button
    
    Args:
        product: MenuItem object
        key_suffix: Unique suffix for button key to avoid conflicts
        language: 'tr' or 'en'
    """
    from utils.session_manager import add_to_cart
    
    # Check if AI is currently processing
    is_disabled = st.session_state.get('ai_is_processing', False)
    
    with st.container():
        col1, col2, col3 = st.columns([3, 2, 2])
        
        with col1:
            st.markdown(f"**{product.name}**")
            st.caption(product.description[:80] + "..." if len(product.description) > 80 else product.description)
        
        with col2:
            st.metric(label="Fiyat" if language == 'tr' else "Price", value=f"{product.price} TL")
        
        with col3:
            button_key = f"add_product_{product.id}_{key_suffix}" if key_suffix else f"add_product_{product.id}"
            if st.button(
                "🛒 Sepete Ekle" if language == 'tr' else "🛒 Add to Cart",
                key=button_key,
                use_container_width=True,
                disabled=is_disabled  # Disable if AI is processing
            ):
                # Add to cart
                add_to_cart(
                    item_id=product.id,
                    item_name=product.name,
                    price=float(product.price),
                    quantity=1
                )
                st.success(f"✅ {product.name} sepete eklendi!" if language == 'tr' else f"✅ {product.name} added to cart!")
                return True
    
    return False


def get_products_from_query(query, language='tr'):
    """
    Get products matching a query using RAG
    """
    try:
        from ai.rag_engine import get_rag_engine
        rag = get_rag_engine()
        docs = rag.search_menu(query, k=5)
        
        # Get unique product IDs
        product_ids = []
        seen = set()
        for doc in docs:
            pid = doc.metadata.get('item_id')
            if pid and pid not in seen:
                product_ids.append(pid)
                seen.add(pid)
        
        return product_ids
    except Exception as e:
        print(f"Error in get_products_from_query: {e}")
        return []


def create_order_confirmation_message(cart_items, total, language='tr'):
    """
    Create order confirmation message
    """
    if language == 'tr':
        items_text = "\n".join([f"• {item['item_name']} x{item['quantity']} = {item['subtotal']:.2f} TL" for item in cart_items])
        return f"""
🛒 **Sepetiniz:**

{items_text}

**Toplam:** {total:.2f} TL

Siparişi onaylamak istiyor musunuz?
"""
    else:
        items_text = "\n".join([f"• {item['item_name']} x{item['quantity']} = {item['subtotal']:.2f} TL" for item in cart_items])
        return f"""
🛒 **Your Cart:**

{items_text}

**Total:** {total:.2f} TL

Would you like to confirm your order?
"""


def parse_ai_response_for_products(response, language='tr'):
    """
    Parse AI response and extract product recommendations
    Returns (product_ids, cleaned_response)
    """
    # Extract product IDs
    product_ids = extract_product_ids_from_response(response)
    
    # Remove product markers from response
    cleaned_response = re.sub(r'\[PRODUCT:\d+\]', '', response)
    
    return product_ids, cleaned_response.strip()
