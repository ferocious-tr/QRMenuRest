"""
Test parse_ai_response_for_products function
"""

from utils.ai_helper import parse_ai_response_for_products

test_response = """Merhaba! Kahvaltı için keyifli seçeneklerimiz var:

1️⃣ **Çıtır Soğan Halkaları** [PRODUCT:3] – 40 TL
2️⃣ **Akdeniz Salatası** [PRODUCT:22] – 55 TL
3️⃣ **Tiramisu** [PRODUCT:31] – 50 TL
4️⃣ **Karışık Pizza** [PRODUCT:14] – 105 TL (şimdiden kahvaltı için biraz farklı bir tat!)

🍴 Sıcak ve lezzetli bir kahvaltı için hemen sipariş verebilirsiniz!

Afiyet olsun! 🌞"""

print("Original response:")
print("="*60)
print(test_response)
print("="*60)
print()

product_ids, clean_text = parse_ai_response_for_products(test_response)

print(f"Extracted Product IDs: {product_ids}")
print()
print("Clean Text:")
print("="*60)
print(clean_text)
print("="*60)
