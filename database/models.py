"""
Database models for QR Menu AI System
Using SQLAlchemy ORM for database operations
"""

from sqlalchemy import create_engine, Column, Integer, String, Float, Boolean, DateTime, ForeignKey, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from datetime import datetime
import os
from dotenv import load_dotenv

load_dotenv()

Base = declarative_base()

# ========================
# MENU MODELS
# ========================

class Category(Base):
    """Menu categories (Appetizers, Main Course, Desserts, etc.)"""
    __tablename__ = 'categories'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False, unique=True)
    name_en = Column(String(100))
    description = Column(Text)
    icon = Column(String(50))  # emoji or icon name
    display_order = Column(Integer, default=0)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.now)
    
    # Relationships
    items = relationship("MenuItem", back_populates="category")


class MenuItem(Base):
    """Individual menu items"""
    __tablename__ = 'menu_items'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    category_id = Column(Integer, ForeignKey('categories.id'), nullable=False)
    name = Column(String(200), nullable=False)
    name_en = Column(String(200))
    description = Column(Text)
    description_en = Column(Text)
    price = Column(Float, nullable=False)
    image_url = Column(String(500))
    
    # Properties
    is_available = Column(Boolean, default=True)
    is_vegetarian = Column(Boolean, default=False)
    is_vegan = Column(Boolean, default=False)
    is_spicy = Column(Boolean, default=False)
    spicy_level = Column(Integer, default=0)  # 0-5
    
    # Allergens and ingredients
    allergens = Column(String(500))  # JSON string: ["nuts", "dairy"]
    ingredients = Column(Text)  # Main ingredients
    
    # Nutrition (optional)
    calories = Column(Integer)
    
    # Popularity
    order_count = Column(Integer, default=0)
    rating = Column(Float, default=0.0)
    
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)
    
    # Relationships
    category = relationship("Category", back_populates="items")
    order_items = relationship("OrderItem", back_populates="menu_item")


# ========================
# TABLE MODELS
# ========================

class Table(Base):
    """Restaurant tables"""
    __tablename__ = 'tables'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    table_number = Column(Integer, nullable=False, unique=True)
    capacity = Column(Integer, default=4)
    qr_code = Column(String(500))  # QR code data/URL
    status = Column(String(20), default='available')  # available, occupied, reserved, cleaning
    current_session_id = Column(String(100))  # UUID for current session
    
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)
    
    # Relationships
    orders = relationship("Order", back_populates="table")


# ========================
# ORDER MODELS
# ========================

class Order(Base):
    """Customer orders"""
    __tablename__ = 'orders'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    order_number = Column(String(20), unique=True, nullable=False)  # ORD-20250106-001
    table_id = Column(Integer, ForeignKey('tables.id'), nullable=False)
    session_id = Column(String(100), nullable=False)  # Links items from same session
    
    # Customer info (optional)
    customer_name = Column(String(100))
    customer_phone = Column(String(20))
    
    # Order details
    status = Column(String(20), default='pending')  # pending, preparing, ready, served, paid, cancelled
    total_amount = Column(Float, default=0.0)
    
    # Customer feedback
    rating = Column(Integer)  # 1-5 stars, only for served orders
    
    # Notes
    special_requests = Column(Text)  # Customer notes
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.now)
    prepared_at = Column(DateTime)
    served_at = Column(DateTime)
    paid_at = Column(DateTime)
    
    # Relationships
    table = relationship("Table", back_populates="orders")
    items = relationship("OrderItem", back_populates="order", cascade="all, delete-orphan")


class OrderItem(Base):
    """Individual items in an order"""
    __tablename__ = 'order_items'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    order_id = Column(Integer, ForeignKey('orders.id'), nullable=False)
    menu_item_id = Column(Integer, ForeignKey('menu_items.id'), nullable=False)
    
    quantity = Column(Integer, default=1)
    unit_price = Column(Float, nullable=False)  # Price at time of order
    subtotal = Column(Float, nullable=False)
    
    # Customization
    notes = Column(Text)  # "Extra cheese", "No onions"
    
    created_at = Column(DateTime, default=datetime.now)
    
    # Relationships
    order = relationship("Order", back_populates="items")
    menu_item = relationship("MenuItem", back_populates="order_items")


# ========================
# CUSTOMER INTERACTION
# ========================

class Restaurant(Base):
    """Restaurant brand information - Single tenant"""
    __tablename__ = 'restaurant'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    
    # Basic Info
    name_tr = Column(String(200), nullable=False, default="Restoran Adı")
    name_en = Column(String(200), nullable=False, default="Restaurant Name")
    
    # Branding
    logo_url = Column(String(500))  # Main logo
    icon_url = Column(String(500))  # Favicon/Icon
    
    # Contact Info
    phone = Column(String(50))
    email = Column(String(100))
    address = Column(Text)
    
    # Description
    about_tr = Column(Text)
    about_en = Column(Text)
    
    # Working Hours
    working_hours = Column(Text)  # JSON string: {"monday": "09:00-22:00", ...}
    
    # Social Media (JSON)
    social_media = Column(Text)  # JSON: {"instagram": "...", "facebook": "...", ...}
    
    # AI Assistant Settings
    ai_welcome_message_tr = Column(Text)  # AI welcome message in Turkish
    ai_welcome_message_en = Column(Text)  # AI welcome message in English
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)


class CustomerReview(Base):
    """Customer reviews and ratings"""
    __tablename__ = 'customer_reviews'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    order_id = Column(Integer, ForeignKey('orders.id'))
    menu_item_id = Column(Integer, ForeignKey('menu_items.id'))
    
    rating = Column(Integer, nullable=False)  # 1-5
    title = Column(String(200))
    review = Column(Text)
    
    created_at = Column(DateTime, default=datetime.now)


class ChatHistory(Base):
    """AI Assistant chat history for analysis"""
    __tablename__ = 'chat_history'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    session_id = Column(String(100), nullable=False)
    table_id = Column(Integer, ForeignKey('tables.id'))
    
    user_message = Column(Text, nullable=False)
    ai_response = Column(Text, nullable=False)
    
    # Metadata
    intent = Column(String(50))  # question, recommendation, order, complaint
    recommended_items = Column(String(500))  # JSON array of item IDs
    
    created_at = Column(DateTime, default=datetime.now)


# ========================
# DATABASE UTILITIES
# ========================

def get_engine():
    """Create database engine"""
    db_url = os.getenv('DATABASE_URL', 'sqlite:///./restaurant.db')
    return create_engine(db_url, echo=False)


def get_session():
    """Get database session"""
    engine = get_engine()
    Session = sessionmaker(bind=engine)
    return Session()


def init_db():
    """Initialize database - create all tables"""
    engine = get_engine()
    Base.metadata.create_all(engine)
    print("✅ Database tables created successfully!")


def drop_all_tables():
    """Drop all tables - use with caution!"""
    engine = get_engine()
    Base.metadata.drop_all(engine)
    print("⚠️ All tables dropped!")


if __name__ == "__main__":
    # Initialize database
    init_db()
