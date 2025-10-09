"""
Test QR Code Generation with Environment Variables
"""

import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.qr_utils import get_base_url, generate_table_qr
from dotenv import load_dotenv

# Load environment
load_dotenv()

def test_qr_generation():
    """Test QR code generation with different configurations"""
    
    print("=" * 70)
    print("QR Code Generation Test")
    print("=" * 70)
    print()
    
    # Get current configuration
    domain = os.getenv('DOMAIN_NAME', '').strip()
    ip = os.getenv('IP_ADDRESS', '').strip()
    port = os.getenv('PORT', '8501')
    
    print("📋 Current Configuration (.env):")
    print(f"   DOMAIN_NAME: {domain if domain else '(not set)'}")
    print(f"   IP_ADDRESS: {ip if ip else '(not set)'}")
    print(f"   PORT: {port}")
    print()
    
    # Get auto-detected base URL
    base_url = get_base_url()
    print(f"🌐 Auto-detected Base URL: {base_url}")
    print()
    
    # Generate test QR code for Table 1
    print("🔄 Generating test QR code for Table 1...")
    print()
    
    try:
        qr_path = generate_table_qr(1)
        print()
        print(f"✅ QR Code generated successfully!")
        print(f"   Saved to: {qr_path}")
        print()
        
        # Show URL examples
        print("📱 URL Examples:")
        print(f"   Table 1: {base_url}/?table=1")
        print(f"   Table 5: {base_url}/?table=5")
        print(f"   Table 10: {base_url}/?table=10")
        print()
        
        print("=" * 70)
        print("Test completed successfully!")
        print("=" * 70)
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return False
    
    return True

if __name__ == "__main__":
    test_qr_generation()
