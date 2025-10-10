"""
Session management utilities for Streamlit
"""

import streamlit as st
import uuid
from datetime import datetime


def init_session_state():
    """Initialize session state variables"""
    
    # User session
    if 'session_id' not in st.session_state:
        st.session_state.session_id = str(uuid.uuid4())
    
    if 'table_number' not in st.session_state:
        st.session_state.table_number = None
    
    if 'table_id' not in st.session_state:
        st.session_state.table_id = None
    
    # Cart
    if 'cart' not in st.session_state:
        st.session_state.cart = []
    
    if 'cart_total' not in st.session_state:
        st.session_state.cart_total = 0.0
    
    # Current order
    if 'current_order_id' not in st.session_state:
        st.session_state.current_order_id = None
    
    # User preferences
    if 'language' not in st.session_state:
        st.session_state.language = 'tr'
    
    # Chat history
    if 'chat_history' not in st.session_state:
        st.session_state.chat_history = []
    
    # AI processing flag
    if 'ai_is_processing' not in st.session_state:
        st.session_state.ai_is_processing = False
    
    # Waiting for order confirmation
    if 'waiting_order_confirmation' not in st.session_state:
        st.session_state.waiting_order_confirmation = False
    
    # Admin/Staff mode
    if 'is_admin' not in st.session_state:
        st.session_state.is_admin = False
    
    # Filters
    if 'show_vegetarian_only' not in st.session_state:
        st.session_state.show_vegetarian_only = False
    
    if 'show_vegan_only' not in st.session_state:
        st.session_state.show_vegan_only = False
    
    if 'allergen_filter' not in st.session_state:
        st.session_state.allergen_filter = []


def get_session_id():
    """Get current session ID"""
    init_session_state()
    return st.session_state.session_id


def get_table_number():
    """Get current table number"""
    init_session_state()
    return st.session_state.table_number


def set_table_number(table_number, table_id):
    """Set table number for current session"""
    st.session_state.table_number = table_number
    st.session_state.table_id = table_id


def add_to_cart(item_id, item_name, price, quantity=1, notes=""):
    """Add item to cart"""
    init_session_state()
    
    # Check if item already exists in cart
    for cart_item in st.session_state.cart:
        if cart_item['item_id'] == item_id and cart_item['notes'] == notes:
            cart_item['quantity'] += quantity
            cart_item['subtotal'] = cart_item['quantity'] * cart_item['price']
            update_cart_total()
            return
    
    # Add new item to cart
    cart_item = {
        'item_id': item_id,
        'item_name': item_name,
        'price': price,
        'quantity': quantity,
        'notes': notes,
        'subtotal': price * quantity
    }
    st.session_state.cart.append(cart_item)
    update_cart_total()


def remove_from_cart(index):
    """Remove item from cart by index"""
    if 0 <= index < len(st.session_state.cart):
        st.session_state.cart.pop(index)
        update_cart_total()


def update_cart_quantity(index, new_quantity):
    """Update quantity of cart item"""
    if 0 <= index < len(st.session_state.cart):
        if new_quantity <= 0:
            remove_from_cart(index)
        else:
            st.session_state.cart[index]['quantity'] = new_quantity
            st.session_state.cart[index]['subtotal'] = (
                st.session_state.cart[index]['price'] * new_quantity
            )
            update_cart_total()


def update_cart_total():
    """Recalculate cart total"""
    total = sum(item['subtotal'] for item in st.session_state.cart)
    st.session_state.cart_total = total


def clear_cart():
    """Clear all items from cart"""
    st.session_state.cart = []
    st.session_state.cart_total = 0.0


def get_cart_count():
    """Get total number of items in cart"""
    return sum(item['quantity'] for item in st.session_state.cart)


def add_chat_message(role, content):
    """Add message to chat history"""
    init_session_state()
    st.session_state.chat_history.append({
        'role': role,  # 'user' or 'assistant'
        'content': content,
        'timestamp': datetime.now()
    })


def clear_chat_history():
    """Clear chat history"""
    st.session_state.chat_history = []


def toggle_admin_mode():
    """Toggle admin mode"""
    st.session_state.is_admin = not st.session_state.is_admin


def switch_language(lang='tr'):
    """Switch language"""
    st.session_state.language = lang
