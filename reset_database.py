"""
Database Reset Script
This script clears all data from the database while preserving the table structure.
Use with caution - this will delete all orders, menu items, categories, etc.
"""

import os
import sys
from datetime import datetime
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from database.models import Base, Category, MenuItem, Table, Order, OrderItem, Restaurant
from database.db_manager import get_db

def confirm_reset():
    """Ask for confirmation before resetting"""
    print("=" * 60)
    print("⚠️  DATABASE RESET WARNING ⚠️")
    print("=" * 60)
    print("\nThis will DELETE ALL DATA from the database:")
    print("  - All orders and order items")
    print("  - All menu items and categories")
    print("  - All table information")
    print("  - All restaurant settings")
    print("  - All customer data")
    print("\nThe table structure will be preserved.")
    print("=" * 60)
    
    response = input("\nAre you sure you want to continue? Type 'YES' to confirm: ")
    return response.strip().upper() == "YES"

def backup_database():
    """Create a backup of the current database"""
    db_path = "restaurant.db"
    if os.path.exists(db_path):
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_path = f"restaurant_backup_{timestamp}.db"
        
        import shutil
        shutil.copy2(db_path, backup_path)
        print(f"✅ Backup created: {backup_path}")
        return backup_path
    return None

def reset_database():
    """Reset all tables in the database"""
    print("\n🔄 Starting database reset...\n")
    
    # Create backup first
    backup_file = backup_database()
    
    db = get_db()
    
    try:
        # Delete in correct order (respecting foreign key constraints)
        print("🗑️  Deleting order items...")
        db.session.query(OrderItem).delete()
        db.session.commit()
        print("   ✓ Order items deleted")
        
        print("🗑️  Deleting orders...")
        db.session.query(Order).delete()
        db.session.commit()
        print("   ✓ Orders deleted")
        
        print("🗑️  Deleting menu items...")
        db.session.query(MenuItem).delete()
        db.session.commit()
        print("   ✓ Menu items deleted")
        
        print("🗑️  Deleting categories...")
        db.session.query(Category).delete()
        db.session.commit()
        print("   ✓ Categories deleted")
        
        print("🗑️  Deleting tables...")
        db.session.query(Table).delete()
        db.session.commit()
        print("   ✓ Tables deleted")
        
        print("🗑️  Deleting restaurant settings...")
        db.session.query(Restaurant).delete()
        db.session.commit()
        print("   ✓ Restaurant settings deleted")
        
        # Reset SQLite sequence numbers
        print("\n🔄 Resetting auto-increment sequences...")
        db.session.execute(text("DELETE FROM sqlite_sequence"))
        db.session.commit()
        print("   ✓ Sequences reset")
        
        print("\n✅ Database reset completed successfully!")
        print(f"\n💾 Backup saved as: {backup_file}")
        print("\n📝 Next steps:")
        print("   1. Run 'python database/init_data.py' to populate initial data")
        print("   2. Or restart the application and add data manually")
        
    except Exception as e:
        db.session.rollback()
        print(f"\n❌ Error during reset: {str(e)}")
        print(f"💾 Your data is safe in backup: {backup_file}")
        sys.exit(1)
    finally:
        db.close()

def main():
    """Main function"""
    print("\n" + "=" * 60)
    print("DATABASE RESET UTILITY")
    print("=" * 60)
    
    if not confirm_reset():
        print("\n❌ Reset cancelled by user.")
        print("No changes were made to the database.")
        sys.exit(0)
    
    reset_database()
    
    print("\n" + "=" * 60)

if __name__ == "__main__":
    main()
