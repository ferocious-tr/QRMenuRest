"""
Add Sample Test Data
Creates realistic test data for development and testing
"""

import os
import sys
from datetime import datetime, timedelta
import random

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from database.models import Category, MenuItem, Table, Order, OrderItem, Restaurant
from database.db_manager import get_db

def create_sample_data():
    """Create comprehensive sample data"""
    print("\n🔄 Creating sample data...\n")
    
    db = get_db()
    
    try:
        # 1. Restaurant Settings
        print("🏢 Creating restaurant settings...")
        restaurant = Restaurant(
            name_tr="Test Restoran",
            name_en="Test Restaurant",
            phone="+90 555 123 4567",
            email="info@testrestaurant.com",
            address="Test Mahallesi, Test Sokak No: 123, İstanbul"
        )
        db.session.add(restaurant)
        db.session.commit()
        print("   ✓ Restaurant created")
        
        # 2. Categories
        print("📁 Creating categories...")
        categories = [
            Category(name="Başlangıçlar", name_en="Appetizers", icon="🥗", display_order=1),
            Category(name="Ana Yemekler", name_en="Main Courses", icon="🍖", display_order=2),
            Category(name="Pizza", name_en="Pizza", icon="🍕", display_order=3),
            Category(name="Tatlılar", name_en="Desserts", icon="🍰", display_order=4),
            Category(name="İçecekler", name_en="Beverages", icon="🥤", display_order=5),
        ]
        for cat in categories:
            db.session.add(cat)
        db.session.commit()
        print(f"   ✓ {len(categories)} categories created")
        
        # 3. Menu Items
        print("🍽️  Creating menu items...")
        menu_items = [
            # Başlangıçlar
            MenuItem(category_id=1, name="Çoban Salata", name_en="Shepherd's Salad", 
                    description="Domates, salatalık, biber, soğan", price=45.00, is_available=True),
            MenuItem(category_id=1, name="Sigara Böreği", name_en="Cheese Rolls", 
                    description="Peynirli kıtır börek", price=55.00, is_available=True),
            MenuItem(category_id=1, name="Humus", name_en="Hummus", 
                    description="Nohut ezmesi, tahin", price=40.00, is_available=True),
            
            # Ana Yemekler
            MenuItem(category_id=2, name="Izgara Köfte", name_en="Grilled Meatballs", 
                    description="200gr dana köfte, pilav, salata", price=150.00, is_available=True),
            MenuItem(category_id=2, name="Tavuk Şiş", name_en="Chicken Kebab", 
                    description="Marine edilmiş tavuk, pilav", price=135.00, is_available=True),
            MenuItem(category_id=2, name="Karışık Izgara", name_en="Mixed Grill", 
                    description="Köfte, tavuk, kuzu", price=220.00, is_available=True),
            
            # Pizza
            MenuItem(category_id=3, name="Margherita Pizza", name_en="Margherita Pizza", 
                    description="Domates sos, mozzarella, fesleğen", price=95.00, is_available=True),
            MenuItem(category_id=3, name="Karışık Pizza", name_en="Mixed Pizza", 
                    description="Sucuk, salam, mantar, mozzarella", price=110.00, is_available=True),
            
            # Tatlılar
            MenuItem(category_id=4, name="Sütlaç", name_en="Rice Pudding", 
                    description="Fırınlanmış sütlaç", price=50.00, is_available=True),
            MenuItem(category_id=4, name="Baklava", name_en="Baklava", 
                    description="Fıstıklı baklava (6 adet)", price=70.00, is_available=True),
            
            # İçecekler
            MenuItem(category_id=5, name="Kola", name_en="Cola", 
                    description="330ml", price=25.00, is_available=True),
            MenuItem(category_id=5, name="Ayran", name_en="Ayran", 
                    description="Ev yapımı", price=20.00, is_available=True),
            MenuItem(category_id=5, name="Türk Kahvesi", name_en="Turkish Coffee", 
                    description="Geleneksel", price=35.00, is_available=True),
        ]
        for item in menu_items:
            db.session.add(item)
        db.session.commit()
        print(f"   ✓ {len(menu_items)} menu items created")
        
        # 4. Tables
        print("🏓 Creating tables...")
        tables = []
        for i in range(1, 11):  # 10 tables
            table = Table(
                table_number=i,
                capacity=4 if i <= 8 else 6,
                status='available'
            )
            tables.append(table)
            db.session.add(table)
        db.session.commit()
        print(f"   ✓ {len(tables)} tables created")
        
        # 5. Sample Orders (last 7 days)
        print("📦 Creating sample orders...")
        statuses = ['paid', 'paid', 'paid', 'served', 'ready', 'preparing', 'pending']
        order_count = 0
        
        for days_ago in range(7):
            order_date = datetime.now() - timedelta(days=days_ago)
            orders_per_day = random.randint(5, 15)
            
            for _ in range(orders_per_day):
                # Random table
                table = random.choice(tables)
                
                # Random status (more paid for older orders)
                if days_ago > 2:
                    status = 'paid'
                else:
                    status = random.choice(statuses)
                
                # Random rating for served/paid orders
                rating = random.randint(3, 5) if status in ['served', 'paid'] else None
                
                # Create order
                order = Order(
                    table_id=table.id,
                    status=status,
                    total_amount=0,  # Will calculate
                    rating=rating,
                    created_at=order_date - timedelta(hours=random.randint(10, 22))
                )
                db.session.add(order)
                db.session.flush()
                
                # Add 1-4 items to order
                num_items = random.randint(1, 4)
                total = 0
                
                for _ in range(num_items):
                    menu_item = random.choice(menu_items)
                    quantity = random.randint(1, 3)
                    subtotal = menu_item.price * quantity
                    
                    order_item = OrderItem(
                        order_id=order.id,
                        menu_item_id=menu_item.id,
                        quantity=quantity,
                        unit_price=menu_item.price,
                        subtotal=subtotal
                    )
                    db.session.add(order_item)
                    total += subtotal
                
                # Update order total
                order.total_amount = total
                order_count += 1
        
        db.session.commit()
        print(f"   ✓ {order_count} orders created")
        
        print("\n✅ Sample data created successfully!\n")
        
        # Show summary
        print("📊 Summary:")
        print(f"   - Restaurant: 1")
        print(f"   - Categories: {len(categories)}")
        print(f"   - Menu Items: {len(menu_items)}")
        print(f"   - Tables: {len(tables)}")
        print(f"   - Orders: {order_count}")
        print()
        
    except Exception as e:
        db.session.rollback()
        print(f"\n❌ Error: {str(e)}")
        sys.exit(1)
    finally:
        db.close()

def main():
    print("\n" + "=" * 60)
    print("SAMPLE DATA GENERATOR")
    print("=" * 60)
    
    db = get_db()
    
    # Check if data already exists
    existing_items = db.session.query(MenuItem).count()
    existing_orders = db.session.query(Order).count()
    
    if existing_items > 0 or existing_orders > 0:
        print(f"\n⚠️  Warning: Database already contains data:")
        print(f"   - Menu Items: {existing_items}")
        print(f"   - Orders: {existing_orders}")
        print("\nThis will add MORE data to existing data.")
        confirm = input("\nContinue? (YES/NO): ").strip().upper()
        
        if confirm != "YES":
            print("\n❌ Cancelled.")
            db.close()
            return
    
    db.close()
    
    create_sample_data()
    
    print("=" * 60)
    print("\n💡 Tip: Run 'streamlit run app.py' to see the data!")
    print()

if __name__ == "__main__":
    main()
