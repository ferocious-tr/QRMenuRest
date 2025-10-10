"""
Advanced Database Reset Script
Offers selective reset options for different data types.
"""

import os
import sys
from datetime import datetime
from sqlalchemy import text

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from database.models import Category, MenuItem, Table, Order, OrderItem, Restaurant
from database.db_manager import get_db

def show_menu():
    """Display reset options menu"""
    print("\n" + "=" * 60)
    print("DATABASE RESET OPTIONS")
    print("=" * 60)
    print("\n1. 🗑️  Reset Everything (All data)")
    print("2. 📦 Reset Orders Only (Keep menu and tables)")
    print("3. 🍽️  Reset Menu Only (Keep orders and tables)")
    print("4. 🏓 Reset Tables Only (Keep orders and menu)")
    print("5. 🔄 Reset Orders + Menu (Keep tables)")
    print("6. ❌ Cancel")
    print("\n" + "=" * 60)

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

def reset_orders(db):
    """Delete all orders and order items"""
    print("🗑️  Deleting order items...")
    db.session.query(OrderItem).delete()
    db.session.commit()
    print("   ✓ Order items deleted")
    
    print("🗑️  Deleting orders...")
    db.session.query(Order).delete()
    db.session.commit()
    print("   ✓ Orders deleted")

def reset_menu(db):
    """Delete all menu items and categories"""
    print("🗑️  Deleting menu items...")
    db.session.query(MenuItem).delete()
    db.session.commit()
    print("   ✓ Menu items deleted")
    
    print("🗑️  Deleting categories...")
    db.session.query(Category).delete()
    db.session.commit()
    print("   ✓ Categories deleted")

def reset_tables(db):
    """Delete all tables"""
    print("🗑️  Deleting tables...")
    db.session.query(Table).delete()
    db.session.commit()
    print("   ✓ Tables deleted")

def reset_restaurant_settings(db):
    """Delete restaurant settings"""
    print("🗑️  Deleting restaurant settings...")
    db.session.query(Restaurant).delete()
    db.session.commit()
    print("   ✓ Restaurant settings deleted")

def reset_sequences(db):
    """Reset auto-increment sequences"""
    print("🔄 Resetting auto-increment sequences...")
    db.session.execute(text("DELETE FROM sqlite_sequence"))
    db.session.commit()
    print("   ✓ Sequences reset")

def show_statistics(db):
    """Show current database statistics"""
    print("\n📊 Current Database Statistics:")
    print("-" * 60)
    
    order_count = db.session.query(Order).count()
    order_item_count = db.session.query(OrderItem).count()
    menu_item_count = db.session.query(MenuItem).count()
    category_count = db.session.query(Category).count()
    table_count = db.session.query(Table).count()
    restaurant_count = db.session.query(Restaurant).count()
    
    print(f"  Orders: {order_count}")
    print(f"  Order Items: {order_item_count}")
    print(f"  Menu Items: {menu_item_count}")
    print(f"  Categories: {category_count}")
    print(f"  Tables: {table_count}")
    print(f"  Restaurant Settings: {restaurant_count}")
    print("-" * 60)

def main():
    """Main function"""
    print("\n" + "=" * 60)
    print("DATABASE RESET UTILITY - ADVANCED MODE")
    print("=" * 60)
    
    db = get_db()
    
    try:
        # Show current statistics
        show_statistics(db)
        
        # Show menu
        show_menu()
        
        choice = input("\nSelect an option (1-6): ").strip()
        
        if choice == "6":
            print("\n❌ Reset cancelled by user.")
            return
        
        if choice not in ["1", "2", "3", "4", "5"]:
            print("\n❌ Invalid option!")
            return
        
        # Confirm action
        print("\n⚠️  WARNING: This action cannot be undone!")
        confirm = input("Type 'YES' to confirm: ").strip().upper()
        
        if confirm != "YES":
            print("\n❌ Reset cancelled by user.")
            return
        
        # Create backup
        backup_file = backup_database()
        
        print("\n🔄 Starting reset operation...\n")
        
        # Execute selected reset
        if choice == "1":
            # Reset everything
            reset_orders(db)
            reset_menu(db)
            reset_tables(db)
            reset_restaurant_settings(db)
            reset_sequences(db)
            
        elif choice == "2":
            # Reset orders only
            reset_orders(db)
            reset_sequences(db)
            
        elif choice == "3":
            # Reset menu only
            reset_menu(db)
            reset_sequences(db)
            
        elif choice == "4":
            # Reset tables only
            # First need to delete orders that reference tables
            if db.session.query(Order).count() > 0:
                print("⚠️  Warning: Deleting tables requires deleting orders first.")
                confirm2 = input("Delete orders too? (YES/NO): ").strip().upper()
                if confirm2 == "YES":
                    reset_orders(db)
            reset_tables(db)
            reset_sequences(db)
            
        elif choice == "5":
            # Reset orders + menu
            reset_orders(db)
            reset_menu(db)
            reset_sequences(db)
        
        print("\n✅ Reset completed successfully!")
        print(f"💾 Backup saved as: {backup_file}")
        
        # Show new statistics
        show_statistics(db)
        
    except Exception as e:
        db.session.rollback()
        print(f"\n❌ Error during reset: {str(e)}")
        sys.exit(1)
    finally:
        db.close()
    
    print("\n" + "=" * 60)

if __name__ == "__main__":
    main()
