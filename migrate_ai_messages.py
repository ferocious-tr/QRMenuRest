"""
Database Migration: Add AI Welcome Message Columns
Adds ai_welcome_message_tr and ai_welcome_message_en columns to Restaurant table
"""

from database.db_manager import get_db
from database.models import Base, Restaurant
from sqlalchemy import text

def migrate_database():
    """Add AI welcome message columns to Restaurant table"""
    print("🔄 Starting database migration...")
    
    db = get_db()
    
    try:
        # Check if columns already exist
        result = db.session.execute(
            text("PRAGMA table_info(restaurant)")
        )
        columns = [row[1] for row in result.fetchall()]
        
        needs_migration = False
        
        if 'ai_welcome_message_tr' not in columns:
            print("  ➕ Adding ai_welcome_message_tr column...")
            db.session.execute(
                text("ALTER TABLE restaurant ADD COLUMN ai_welcome_message_tr TEXT")
            )
            needs_migration = True
        else:
            print("  ✓ ai_welcome_message_tr column already exists")
        
        if 'ai_welcome_message_en' not in columns:
            print("  ➕ Adding ai_welcome_message_en column...")
            db.session.execute(
                text("ALTER TABLE restaurant ADD COLUMN ai_welcome_message_en TEXT")
            )
            needs_migration = True
        else:
            print("  ✓ ai_welcome_message_en column already exists")
        
        if needs_migration:
            db.session.commit()
            print("✅ Migration completed successfully!")
            
            # Set default messages
            print("\n📝 Setting default AI welcome messages...")
            restaurant = db.get_restaurant_info()
            
            if restaurant and not restaurant.ai_welcome_message_tr:
                default_tr = """Merhaba! 👋 Ben sizin AI menü asistanınızım.

Size yemek önerilerinde bulunabilir, sorularınızı cevaplayabilir ve menümüzü keşfetmenize yardımcı olabilirim.

🍕 Vejetaryen/vegan seçenekler
🌶️ Acılık tercihleri
💰 Bütçenize uygun öneriler
⚠️ Alerjen bilgileri

Nasıl yardımcı olabilirim?"""
                
                default_en = """Hello! 👋 I'm your AI menu assistant.

I can provide meal recommendations, answer your questions, and help you explore our menu.

🍕 Vegetarian/vegan options
🌶️ Spiciness preferences
💰 Budget-friendly suggestions
⚠️ Allergen information

How can I help you?"""
                
                db.update_restaurant_info(
                    ai_welcome_message_tr=default_tr,
                    ai_welcome_message_en=default_en
                )
                print("✅ Default messages set!")
        else:
            print("✅ No migration needed - database is up to date")
        
        db.close()
        
    except Exception as e:
        print(f"❌ Migration failed: {e}")
        db.session.rollback()
        db.close()
        raise

if __name__ == "__main__":
    print("="*60)
    print("AI Welcome Message Migration")
    print("="*60)
    print()
    
    migrate_database()
    
    print()
    print("="*60)
    print("Migration complete! You can now use the AI Assistant tab")
    print("in Brand Management to customize welcome messages.")
    print("="*60)
