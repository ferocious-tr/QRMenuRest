"""
QR Code Generator and Scanner utilities
"""

import qrcode
from PIL import Image
import os
from datetime import datetime
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


def generate_qr_code(data, filename=None, save_path="static/qr_codes"):
    """
    Generate QR code for table
    
    Args:
        data: URL or data to encode
        filename: Output filename (auto-generated if None)
        save_path: Directory to save QR codes
    
    Returns:
        Path to saved QR code image
    """
    # Create directory if not exists
    os.makedirs(save_path, exist_ok=True)
    
    # Generate filename if not provided
    if filename is None:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"qr_{timestamp}.png"
    
    # Ensure .png extension
    if not filename.endswith('.png'):
        filename += '.png'
    
    filepath = os.path.join(save_path, filename)
    
    # Generate QR code
    qr = qrcode.QRCode(
        version=1,  # Size of QR code (1-40)
        error_correction=qrcode.constants.ERROR_CORRECT_H,  # High error correction
        box_size=10,  # Size of each box in pixels
        border=4,  # Border size in boxes
    )
    
    qr.add_data(data)
    qr.make(fit=True)
    
    # Create image
    img = qr.make_image(fill_color="black", back_color="white")
    
    # Add logo (optional)
    # You can add your restaurant logo in the center
    
    # Save image
    img.save(filepath)
    
    return filepath


def get_base_url():
    """
    Get base URL from environment variables
    Priority: DOMAIN_NAME > IP_ADDRESS > localhost
    
    Returns:
        Base URL string
    """
    domain = os.getenv('DOMAIN_NAME', '').strip()
    ip_address = os.getenv('IP_ADDRESS', '').strip()
    port = os.getenv('PORT', '8501').strip()
    
    # If domain is set, use it (production)
    if domain:
        # Add http:// if not present
        if not domain.startswith(('http://', 'https://')):
            domain = f"https://{domain}"
        return domain
    
    # If IP address is set, use it (local network)
    if ip_address:
        return f"http://{ip_address}:{port}"
    
    # Fallback to localhost (development)
    return f"http://localhost:{port}"


def generate_table_qr(table_number, base_url=None):
    """
    Generate QR code for a specific table
    
    Args:
        table_number: Table number
        base_url: Base URL of the application (auto-detected from .env if None)
    
    Returns:
        Path to saved QR code image
    """
    # Auto-detect base URL from environment if not provided
    if base_url is None:
        base_url = get_base_url()
    
    # Create URL with table parameter
    url = f"{base_url}/?table={table_number}"
    
    filename = f"table_{table_number}.png"
    filepath = generate_qr_code(url, filename)
    
    print(f"✅ QR code generated for Table {table_number}")
    print(f"   URL: {url}")
    print(f"   File: {filepath}")
    return filepath


def generate_all_table_qrs(num_tables=20, base_url=None):
    """
    Generate QR codes for all tables
    
    Args:
        num_tables: Number of tables
        base_url: Base URL of the application (auto-detected from .env if None)
    
    Returns:
        List of generated file paths
    """
    # Auto-detect base URL from environment if not provided
    if base_url is None:
        base_url = get_base_url()
    
    paths = []
    print(f"🔄 Generating QR codes for {num_tables} tables...")
    print(f"📍 Base URL: {base_url}")
    print("")
    
    for table_num in range(1, num_tables + 1):
        path = generate_table_qr(table_num, base_url)
        paths.append(path)
    
    print("")
    print(f"✅ Generated {len(paths)} QR codes successfully!")
    return paths


def scan_qr_code(image_path):
    """
    Scan QR code from image (for testing)
    
    Args:
        image_path: Path to QR code image
    
    Returns:
        Decoded data or None
    """
    try:
        from pyzbar.pyzbar import decode
        from PIL import Image
        
        img = Image.open(image_path)
        decoded_objects = decode(img)
        
        if decoded_objects:
            return decoded_objects[0].data.decode('utf-8')
        return None
    except Exception as e:
        print(f"Error scanning QR code: {e}")
        return None


if __name__ == "__main__":
    # Test: Generate QR codes for all tables
    generate_all_table_qrs()
