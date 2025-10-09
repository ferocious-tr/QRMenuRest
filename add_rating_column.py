"""
Migration script to add rating column to orders table
"""

import sqlite3
import os

def add_rating_column():
    """Add rating column to orders table if it doesn't exist"""
    
    db_path = "restaurant.db"
    
    if not os.path.exists(db_path):
        print(f"❌ Database not found: {db_path}")
        return False
    
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Check if column already exists
        cursor.execute("PRAGMA table_info(orders)")
        columns = [col[1] for col in cursor.fetchall()]
        
        if 'rating' in columns:
            print("✅ Rating column already exists in orders table")
            return True
        
        # Add rating column
        cursor.execute("""
            ALTER TABLE orders 
            ADD COLUMN rating INTEGER
        """)
        
        conn.commit()
        print("✅ Successfully added rating column to orders table")
        
        # Verify
        cursor.execute("PRAGMA table_info(orders)")
        columns = [col[1] for col in cursor.fetchall()]
        print(f"📋 Orders table columns: {', '.join(columns)}")
        
        conn.close()
        return True
        
    except Exception as e:
        print(f"❌ Error adding rating column: {e}")
        if 'conn' in locals():
            conn.close()
        return False

if __name__ == "__main__":
    print("🔧 Adding rating column to orders table...")
    print("-" * 50)
    success = add_rating_column()
    print("-" * 50)
    
    if success:
        print("✅ Migration completed successfully!")
    else:
        print("❌ Migration failed!")
