"""
Database Manager - CRUD operations for the restaurant system
"""

from sqlalchemy.orm import Session
from sqlalchemy import desc, func
from database.models import (
    Category, MenuItem, Table, Order, OrderItem, 
    CustomerReview, ChatHistory, Restaurant, get_session
)
from datetime import datetime
import json
from typing import List, Optional


class DatabaseManager:
    """Centralized database operations"""
    
    def __init__(self):
        self.session = get_session()
    
    def close(self):
        """Close database session"""
        self.session.close()
    
    # ========================
    # CATEGORY OPERATIONS
    # ========================
    
    def get_all_categories(self, active_only=True):
        """Get all categories"""
        query = self.session.query(Category)
        if active_only:
            query = query.filter(Category.is_active == True)
        return query.order_by(Category.display_order).all()
    
    def create_category(self, name, name_en=None, description=None, icon=None):
        """Create new category"""
        category = Category(
            name=name,
            name_en=name_en,
            description=description,
            icon=icon
        )
        self.session.add(category)
        self.session.commit()
        return category
    
    # ========================
    # MENU ITEM OPERATIONS
    # ========================
    
    def get_menu_items_by_category(self, category_id, available_only=True):
        """Get menu items by category"""
        query = self.session.query(MenuItem).filter(MenuItem.category_id == category_id)
        if available_only:
            query = query.filter(MenuItem.is_available == True)
        return query.all()
    
    def get_all_menu_items(self, available_only=True):
        """Get all menu items"""
        query = self.session.query(MenuItem)
        if available_only:
            query = query.filter(MenuItem.is_available == True)
        return query.all()
    
    def get_menu_item_by_id(self, item_id):
        """Get single menu item"""
        return self.session.query(MenuItem).filter(MenuItem.id == item_id).first()
    
    def search_menu_items(self, search_term, available_only=True):
        """Search menu items by name or description"""
        query = self.session.query(MenuItem).filter(
            (MenuItem.name.contains(search_term)) | 
            (MenuItem.description.contains(search_term))
        )
        if available_only:
            query = query.filter(MenuItem.is_available == True)
        return query.all()
    
    def get_popular_items(self, limit=10):
        """Get most popular items"""
        return self.session.query(MenuItem)\
            .filter(MenuItem.is_available == True)\
            .order_by(desc(MenuItem.order_count))\
            .limit(limit).all()
    
    def get_vegetarian_items(self):
        """Get vegetarian items"""
        return self.session.query(MenuItem)\
            .filter(MenuItem.is_vegetarian == True, MenuItem.is_available == True)\
            .all()
    
    def create_menu_item(self, **kwargs):
        """Create new menu item"""
        item = MenuItem(**kwargs)
        self.session.add(item)
        self.session.commit()
        return item
    
    def update_menu_item(self, item_id, **kwargs):
        """Update menu item"""
        item = self.get_menu_item_by_id(item_id)
        if item:
            for key, value in kwargs.items():
                setattr(item, key, value)
            item.updated_at = datetime.now()
            self.session.commit()
        return item
    
    # ========================
    # TABLE OPERATIONS
    # ========================
    
    def get_all_tables(self):
        """Get all tables"""
        return self.session.query(Table).order_by(Table.table_number).all()
    
    def get_table_by_number(self, table_number):
        """Get table by number"""
        return self.session.query(Table).filter(Table.table_number == table_number).first()
    
    def get_table_by_id(self, table_id):
        """Get table by ID"""
        return self.session.query(Table).filter(Table.id == table_id).first()
    
    def update_table_status(self, table_id, status, session_id=None):
        """Update table status"""
        table = self.get_table_by_id(table_id)
        if table:
            table.status = status
            if session_id:
                table.current_session_id = session_id
            table.updated_at = datetime.now()
            self.session.commit()
        return table
    
    def create_table(self, table_number, capacity=4, qr_code=None):
        """Create new table"""
        table = Table(
            table_number=table_number,
            capacity=capacity,
            qr_code=qr_code
        )
        self.session.add(table)
        self.session.commit()
        return table
    
    # ========================
    # ORDER OPERATIONS
    # ========================
    
    def create_order(self, table_id, session_id, order_number=None):
        """Create new order"""
        if not order_number:
            # Generate order number: ORD-20250106-001
            today = datetime.now().strftime("%Y%m%d")
            count = self.session.query(Order).filter(
                func.DATE(Order.created_at) == datetime.now().date()
            ).count()
            order_number = f"ORD-{today}-{count+1:03d}"
        
        order = Order(
            order_number=order_number,
            table_id=table_id,
            session_id=session_id
        )
        self.session.add(order)
        self.session.commit()
        return order
    
    def get_order_by_id(self, order_id):
        """Get order by ID"""
        return self.session.query(Order).filter(Order.id == order_id).first()
    
    def get_orders_by_table(self, table_id, session_id=None):
        """Get orders for a table"""
        query = self.session.query(Order).filter(Order.table_id == table_id)
        if session_id:
            query = query.filter(Order.session_id == session_id)
        return query.all()
    
    def get_today_orders_by_table(self, table_id):
        """Get today's orders for a table"""
        from datetime import datetime, date
        today_start = datetime.combine(date.today(), datetime.min.time())
        return self.session.query(Order).filter(
            Order.table_id == table_id,
            Order.created_at >= today_start
        ).order_by(Order.created_at.desc()).all()
    
    def get_orders_by_table_and_date_range(self, table_id=None, start_date=None, end_date=None):
        """Get orders by table and date range"""
        from datetime import datetime, timedelta
        
        query = self.session.query(Order)
        
        # Filter by table if provided
        if table_id:
            query = query.filter(Order.table_id == table_id)
        
        # Filter by date range
        if start_date:
            start_datetime = datetime.combine(start_date, datetime.min.time())
            query = query.filter(Order.created_at >= start_datetime)
        
        if end_date:
            end_datetime = datetime.combine(end_date, datetime.max.time())
            query = query.filter(Order.created_at <= end_datetime)
        
        return query.order_by(Order.created_at.desc()).all()
    
    def get_active_orders(self):
        """Get all active orders (not paid or cancelled) - ordered by newest first"""
        return self.session.query(Order).filter(
            Order.status.in_(['pending', 'preparing', 'ready', 'served'])
        ).order_by(Order.created_at.desc()).all()
    
    def update_order_status(self, order_id, status):
        """Update order status"""
        order = self.get_order_by_id(order_id)
        if order:
            order.status = status
            if status == 'preparing':
                order.prepared_at = datetime.now()
            elif status == 'served':
                order.served_at = datetime.now()
            elif status == 'paid':
                order.paid_at = datetime.now()
            self.session.commit()
        return order
    
    def add_order_item(self, order_id, menu_item_id, quantity=1, notes=None):
        """Add item to order"""
        menu_item = self.get_menu_item_by_id(menu_item_id)
        if not menu_item:
            return None
        
        unit_price = menu_item.price
        subtotal = unit_price * quantity
        
        order_item = OrderItem(
            order_id=order_id,
            menu_item_id=menu_item_id,
            quantity=quantity,
            unit_price=unit_price,
            subtotal=subtotal,
            notes=notes
        )
        self.session.add(order_item)
        
        # Update order total
        order = self.get_order_by_id(order_id)
        if order:
            order.total_amount += subtotal
        
        # Update item order count
        menu_item.order_count += quantity
        
        self.session.commit()
        return order_item
    
    def get_order_items(self, order_id):
        """Get all items in an order"""
        return self.session.query(OrderItem).filter(OrderItem.order_id == order_id).all()
    
    # ========================
    # CHAT HISTORY
    # ========================
    
    def save_chat_message(self, session_id, user_message, ai_response, 
                          table_id=None, intent=None, recommended_items=None):
        """Save chat interaction"""
        chat = ChatHistory(
            session_id=session_id,
            table_id=table_id,
            user_message=user_message,
            ai_response=ai_response,
            intent=intent,
            recommended_items=json.dumps(recommended_items) if recommended_items else None
        )
        self.session.add(chat)
        self.session.commit()
        return chat
    
    def get_chat_history(self, session_id, limit=50):
        """Get chat history for a session"""
        return self.session.query(ChatHistory)\
            .filter(ChatHistory.session_id == session_id)\
            .order_by(ChatHistory.created_at)\
            .limit(limit).all()
    
    # ========================
    # STATISTICS
    # ========================
    
    def get_daily_stats(self):
        """Get today's statistics"""
        today = datetime.now().date()
        
        total_orders = self.session.query(Order).filter(
            func.DATE(Order.created_at) == today
        ).count()
        
        total_revenue = self.session.query(func.sum(Order.total_amount)).filter(
            func.DATE(Order.created_at) == today,
            Order.status == 'paid'
        ).scalar() or 0
        
        return {
            'total_orders': total_orders,
            'total_revenue': total_revenue,
            'date': today
        }
    
    # ========================
    # RESTAURANT/BRAND OPERATIONS
    # ========================
    
    def get_restaurant_info(self):
        """Get restaurant information (single tenant - returns first record)"""
        restaurant = self.session.query(Restaurant).first()
        if not restaurant:
            # Create default restaurant if not exists
            restaurant = self.create_default_restaurant()
        return restaurant
    
    def create_default_restaurant(self):
        """Create default restaurant record"""
        restaurant = Restaurant(
            name_tr="La Pizza Bella",
            name_en="La Pizza Bella",
            about_tr="Geleneksel İtalyan lezzetleriyle hizmetinizdeyiz.",
            about_en="Serving traditional Italian flavors.",
            phone="+90 212 XXX XX XX",
            email="info@lapizzabella.com",
            address="İstanbul, Türkiye",
            working_hours=json.dumps({
                "Pazartesi": "10:00 - 23:00",
                "Salı": "10:00 - 23:00",
                "Çarşamba": "10:00 - 23:00",
                "Perşembe": "10:00 - 23:00",
                "Cuma": "10:00 - 00:00",
                "Cumartesi": "10:00 - 00:00",
                "Pazar": "10:00 - 23:00"
            }),
            social_media=json.dumps({
                "instagram": "",
                "facebook": "",
                "twitter": "",
                "youtube": ""
            })
        )
        self.session.add(restaurant)
        self.session.commit()
        return restaurant
    
    def update_restaurant_info(self, **kwargs):
        """Update restaurant information"""
        restaurant = self.get_restaurant_info()
        
        # Update allowed fields
        allowed_fields = [
            'name_tr', 'name_en', 'logo_url', 'icon_url',
            'phone', 'email', 'address', 'about_tr', 'about_en',
            'working_hours', 'social_media'
        ]
        
        for key, value in kwargs.items():
            if key in allowed_fields and value is not None:
                setattr(restaurant, key, value)
        
        restaurant.updated_at = datetime.now()
        self.session.commit()
        return restaurant


# Convenience functions
def get_db():
    """Get database manager instance"""
    return DatabaseManager()


if __name__ == "__main__":
    db = get_db()
    print("✅ Database Manager initialized successfully!")
    db.close()
