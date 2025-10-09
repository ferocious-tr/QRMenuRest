"""
Initialize database with sample data
Run this script once to populate the database
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from database.models import init_db, get_session, Category, MenuItem, Table
import pandas as pd


def init_sample_data():
    """Initialize database with sample menu data"""
    
    print("🔧 Initializing database...")
    init_db()
    
    session = get_session()
    
    # Check if data already exists
    if session.query(Category).count() > 0:
        print("⚠️  Database already has data. Skipping initialization.")
        return
    
    print("📋 Creating categories...")
    categories = {
        'Başlangıçlar': {'name_en': 'Appetizers', 'icon': '🥗', 'order': 1},
        'Pizzalar': {'name_en': 'Pizzas', 'icon': '🍕', 'order': 2},
        'Ana Yemekler': {'name_en': 'Main Courses', 'icon': '🍗', 'order': 3},
        'Pastalar': {'name_en': 'Pasta', 'icon': '🍝', 'order': 4},
        'Salatalar': {'name_en': 'Salads', 'icon': '🥗', 'order': 5},
        'İçecekler': {'name_en': 'Beverages', 'icon': '🥤', 'order': 6},
        'Tatlılar': {'name_en': 'Desserts', 'icon': '🍰', 'order': 7},
    }
    
    category_map = {}
    for name, info in categories.items():
        cat = Category(
            name=name,
            name_en=info['name_en'],
            icon=info['icon'],
            display_order=info['order']
        )
        session.add(cat)
        session.flush()  # Get the ID
        category_map[name] = cat.id
    
    session.commit()
    print(f"✅ Created {len(categories)} categories")
    
    print("🍽️  Loading menu items from CSV...")
    df = pd.read_csv('data/menu_items.csv')
    
    item_count = 0
    for _, row in df.iterrows():
        item = MenuItem(
            category_id=category_map[row['Category']],
            name=row['Name'],
            name_en=row['Name_EN'],
            description=row['Description'],
            description_en=row['Description_EN'],
            price=row['Price'],
            is_vegetarian=bool(row['Is_Vegetarian']),
            is_vegan=bool(row['Is_Vegan']),
            is_spicy=bool(row['Is_Spicy']),
            spicy_level=int(row['Spicy_Level']),
            allergens=row['Allergens'],
            ingredients=row['Ingredients'],
            calories=int(row['Calories']) if pd.notna(row['Calories']) else None,
            is_available=True
        )
        session.add(item)
        item_count += 1
    
    session.commit()
    print(f"✅ Created {item_count} menu items")
    
    print("🏓 Creating tables...")
    for i in range(1, 21):  # Create 20 tables
        table = Table(
            table_number=i,
            capacity=4 if i <= 15 else 6,  # Tables 16-20 have larger capacity
            status='available'
        )
        session.add(table)
    
    session.commit()
    print("✅ Created 20 tables")
    
    session.close()
    print("\n🎉 Database initialization completed successfully!")
    print("🚀 You can now run: streamlit run app.py")


if __name__ == "__main__":
    init_sample_data()
