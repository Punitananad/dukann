"""
Run this after migrations to seed sample data:
    python setup.py
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'shop_locator.settings')
django.setup()

from django.contrib.auth.models import User
from racks.models import Rack, Shelf
from products.models import Product

print("Setting up RackFinder sample data...")

# ── Superuser ──────────────────────────────────────────────────────────────
if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser('admin', 'admin@shop.local', 'admin123')
    print("  Created superuser: admin / admin123")
else:
    print("  Superuser already exists")

# ── Racks ──────────────────────────────────────────────────────────────────
racks_data = [
    ('A', 'Lipsticks & Lip Products'),
    ('B', 'Foundation & Concealer'),
    ('C', 'Face Cream & Moisturizer'),
    ('D', 'Hair Products'),
    ('E', 'Perfumes & Deodorants'),
]

racks = {}
for name, category in racks_data:
    rack, created = Rack.objects.get_or_create(name=name, defaults={'category': category})
    racks[name] = rack
    if created:
        print(f"  Created Rack {name} — {category}")

# ── Shelves ────────────────────────────────────────────────────────────────
shelf_counts = {'A': 4, 'B': 3, 'C': 4, 'D': 3, 'E': 3}
shelves = {}
for rack_name, count in shelf_counts.items():
    rack = racks[rack_name]
    for i in range(1, count + 1):
        code = f"{rack_name}{i}"
        shelf, created = Shelf.objects.get_or_create(rack=rack, code=code)
        shelves[code] = shelf
        if created:
            print(f"    Created Shelf {code}")

# ── Products ───────────────────────────────────────────────────────────────
products_data = [
    ('Lipstick Ruby Red', 'Lakme', 'Lipstick', 'A', 'A1', 12),
    ('Lipstick Coral Bliss', 'Lakme', 'Lipstick', 'A', 'A1', 8),
    ('Matte Lipstick Nude', 'Maybelline', 'Lipstick', 'A', 'A2', 15),
    ('Super Stay Lipstick', 'Maybelline', 'Lipstick', 'A', 'A2', 3),
    ('Lip Gloss Pink', 'NYX', 'Lip Gloss', 'A', 'A3', 20),
    ('Lip Liner Brown', 'Faces Canada', 'Lip Liner', 'A', 'A4', 10),

    ('Fit Me Foundation', 'Maybelline', 'Foundation', 'B', 'B1', 7),
    ('Skin Tint SPF30', 'Lakme', 'Foundation', 'B', 'B1', 5),
    ('Stay Matte Concealer', 'NYX', 'Concealer', 'B', 'B2', 11),
    ('HD Foundation', 'L\'Oreal', 'Foundation', 'B', 'B3', 0),

    ('Olay Regenerist Cream', 'Olay', 'Face Cream', 'C', 'C1', 6),
    ('Pond\'s White Beauty', 'Pond\'s', 'Face Cream', 'C', 'C1', 9),
    ('Neutrogena Moisturizer', 'Neutrogena', 'Moisturizer', 'C', 'C2', 4),
    ('Vitamin C Serum', 'Minimalist', 'Serum', 'C', 'C3', 14),
    ('Sunscreen SPF50', 'Neutrogena', 'Sunscreen', 'C', 'C4', 18),

    ('Coconut Hair Oil', 'Parachute', 'Hair Oil', 'D', 'D1', 22),
    ('Anti-Dandruff Shampoo', 'Head & Shoulders', 'Shampoo', 'D', 'D2', 8),
    ('Keratin Conditioner', 'TRESemmé', 'Conditioner', 'D', 'D3', 6),

    ('Eau de Parfum Rose', 'Yardley', 'Perfume', 'E', 'E1', 3),
    ('Deo Spray Fresh', 'Nivea', 'Deodorant', 'E', 'E2', 16),
    ('Body Mist Jasmine', 'The Body Shop', 'Body Mist', 'E', 'E3', 9),
]

for name, brand, category, rack_name, shelf_code, qty in products_data:
    rack = racks.get(rack_name)
    shelf = shelves.get(shelf_code)
    product, created = Product.objects.get_or_create(
        name=name, brand=brand,
        defaults={
            'category': category,
            'rack': rack,
            'shelf': shelf,
            'quantity': qty,
        }
    )
    if created:
        print(f"  Product: {brand} {name} -> {shelf_code}")

print("\n[OK] Setup complete!")
print("  URL:      http://127.0.0.1:8000/")
print("  Login:    admin")
print("  Password: admin123")
