"""
Management command to seed the database with cosmetic products.
Usage: python manage.py seed_products
"""

from django.core.management.base import BaseCommand
from products.models import Product
from racks.models import Wall, Rack

PRODUCTS = [
    # ── FACE WASH ──────────────────────────────────────────────────────────
    {"name": "Himalaya Purifying Neem Face Wash", "category": "Skincare", "subcategory": "Face Wash",
     "tags": "neem, purifying, oily skin, acne", "search_keywords": "face wash cleanser foaming daily"},
    {"name": "Cetaphil Gentle Skin Cleanser", "category": "Skincare", "subcategory": "Face Wash",
     "tags": "gentle, sensitive skin, soap-free", "search_keywords": "face wash cleanser dry skin"},
    {"name": "Neutrogena Deep Clean Facial Cleanser", "category": "Skincare", "subcategory": "Face Wash",
     "tags": "deep clean, oil control, salicylic", "search_keywords": "face wash cleanser pores blackhead"},
    {"name": "Pond's Bright Beauty Face Wash", "category": "Skincare", "subcategory": "Face Wash",
     "tags": "brightening, vitamin c, glow", "search_keywords": "face wash cleanser glowing fairness"},
    {"name": "Plum Green Tea Pore Cleansing Face Wash", "category": "Skincare", "subcategory": "Face Wash",
     "tags": "green tea, pore control, anti-oxidant", "search_keywords": "face wash cleanser oily acne vegan"},

    # ── MOISTURIZER ────────────────────────────────────────────────────────
    {"name": "Nivea Soft Light Moisturising Cream", "category": "Skincare", "subcategory": "Moisturizer",
     "tags": "light, jojoba oil, vitamin e", "search_keywords": "moisturizer cream lotion daily hydration"},
    {"name": "Lakme Peach Milk Moisturizer", "category": "Skincare", "subcategory": "Moisturizer",
     "tags": "peach, milk, non-greasy, spf 24", "search_keywords": "moisturizer lotion sunscreen daily"},
    {"name": "Dot & Key Watermelon Cooling Moisturizer", "category": "Skincare", "subcategory": "Moisturizer",
     "tags": "watermelon, cooling, hyaluronic acid", "search_keywords": "moisturizer gel hydrating summer"},
    {"name": "CeraVe Moisturizing Cream", "category": "Skincare", "subcategory": "Moisturizer",
     "tags": "ceramides, hyaluronic acid, dry skin", "search_keywords": "moisturizer cream body face lotion"},
    {"name": "Vaseline Intensive Care Aloe Soothe Lotion", "category": "Skincare", "subcategory": "Moisturizer",
     "tags": "aloe vera, soothing, body lotion", "search_keywords": "moisturizer lotion body cream"},

    # ── SUNSCREEN ──────────────────────────────────────────────────────────
    {"name": "Neutrogena Ultra Sheer Sunscreen SPF 50+", "category": "Skincare", "subcategory": "Sunscreen",
     "tags": "spf 50, broad spectrum, non-greasy", "search_keywords": "sunscreen sunblock spf uv protection"},
    {"name": "Lakme Sun Expert SPF 50 Sunscreen", "category": "Skincare", "subcategory": "Sunscreen",
     "tags": "spf 50, pa+++, matte finish", "search_keywords": "sunscreen sunblock spf uv"},
    {"name": "Re'equil Ultra Matte Dry Touch Sunscreen SPF 50", "category": "Skincare", "subcategory": "Sunscreen",
     "tags": "spf 50, matte, no white cast", "search_keywords": "sunscreen sunblock spf dry touch"},
    {"name": "Minimalist SPF 50 Sunscreen", "category": "Skincare", "subcategory": "Sunscreen",
     "tags": "spf 50, hyaluronic acid, lightweight", "search_keywords": "sunscreen sunblock spf minimal"},

    # ── SERUM ──────────────────────────────────────────────────────────────
    {"name": "The Ordinary Niacinamide 10% + Zinc 1% Serum", "category": "Skincare", "subcategory": "Serum",
     "tags": "niacinamide, zinc, pores, blemish", "search_keywords": "serum face treatment pore skin"},
    {"name": "Minimalist Vitamin C 10% Serum", "category": "Skincare", "subcategory": "Serum",
     "tags": "vitamin c, brightening, anti-oxidant", "search_keywords": "serum glow brightening dark spots"},
    {"name": "Plum 15% Vitamin C Serum", "category": "Skincare", "subcategory": "Serum",
     "tags": "vitamin c, glow, dark spots, vegan", "search_keywords": "serum face brightening pigmentation"},
    {"name": "Dot & Key Barrier Repair Ceramide Serum", "category": "Skincare", "subcategory": "Serum",
     "tags": "ceramide, barrier, hydration, repair", "search_keywords": "serum face hydrating skin repair"},

    # ── TONER ──────────────────────────────────────────────────────────────
    {"name": "Minimalist AHA BHA Exfoliating Toner", "category": "Skincare", "subcategory": "Toner",
     "tags": "aha, bha, exfoliating, pores", "search_keywords": "toner face exfoliant acid skin"},
    {"name": "Plum Green Tea Alcohol-Free Toner", "category": "Skincare", "subcategory": "Toner",
     "tags": "green tea, alcohol-free, hydrating", "search_keywords": "toner face refresh hydrate"},
    {"name": "Neutrogena Alcohol-Free Toner", "category": "Skincare", "subcategory": "Toner",
     "tags": "alcohol-free, sensitive, gentle", "search_keywords": "toner face balance skin"},

    # ── LIPSTICK ───────────────────────────────────────────────────────────
    {"name": "Lakme Absolute Matte Lipstick - Red", "category": "Makeup", "subcategory": "Lipstick",
     "tags": "matte, red, bold, long-lasting", "search_keywords": "lipstick lip color lip colour"},
    {"name": "Lakme Absolute Matte Lipstick - Nude", "category": "Makeup", "subcategory": "Lipstick",
     "tags": "matte, nude, everyday", "search_keywords": "lipstick lip color nude"},
    {"name": "Maybelline SuperStay Matte Ink Lipstick - Pink", "category": "Makeup", "subcategory": "Lipstick",
     "tags": "matte, pink, 16hr, smudge-proof", "search_keywords": "lipstick lip color long lasting"},
    {"name": "Nykaa So Matte! Lipstick - Berry", "category": "Makeup", "subcategory": "Lipstick",
     "tags": "matte, berry, bold", "search_keywords": "lipstick lip color bold dark"},
    {"name": "Colorbar Velvet Matte Lipstick - Coral", "category": "Makeup", "subcategory": "Lipstick",
     "tags": "velvet, coral, matte, creamy", "search_keywords": "lipstick lip color coral summer"},

    # ── EYELINER ───────────────────────────────────────────────────────────
    {"name": "Lakme Eyeconic Kajal", "category": "Makeup", "subcategory": "Eyeliner",
     "tags": "kajal, kohl, smoky, black", "search_keywords": "eyeliner kajal kohl eye black"},
    {"name": "Maybelline Colossal Kajal", "category": "Makeup", "subcategory": "Eyeliner",
     "tags": "kajal, 12hr, smudge-proof, black", "search_keywords": "eyeliner kajal eye liner black"},
    {"name": "Nykaa Eyes On Me! Felt Tip Eyeliner", "category": "Makeup", "subcategory": "Eyeliner",
     "tags": "felt tip, liquid, precise, black", "search_keywords": "eyeliner liquid pen eye liner"},
    {"name": "Swiss Beauty Waterproof Gel Eyeliner", "category": "Makeup", "subcategory": "Eyeliner",
     "tags": "gel, waterproof, intense, black", "search_keywords": "eyeliner gel eye liner waterproof"},

    # ── MASCARA ────────────────────────────────────────────────────────────
    {"name": "Maybelline Colossal Volum' Express Mascara", "category": "Makeup", "subcategory": "Mascara",
     "tags": "volume, black, collagen, curling", "search_keywords": "mascara lashes volume curl"},
    {"name": "Lakme Eyeconic Curling Mascara", "category": "Makeup", "subcategory": "Mascara",
     "tags": "curling, thickening, 24hr", "search_keywords": "mascara lashes curl volume"},
    {"name": "L'Oreal Paris Miss Manga Mascara", "category": "Makeup", "subcategory": "Mascara",
     "tags": "dramatic, volume, fanned", "search_keywords": "mascara lashes bold dramatic"},

    # ── FOUNDATION ─────────────────────────────────────────────────────────
    {"name": "Lakme 9to5 Primer + Matte Foundation", "category": "Makeup", "subcategory": "Foundation",
     "tags": "matte, primer, full coverage, spf", "search_keywords": "foundation face base coverage"},
    {"name": "Maybelline Fit Me Matte + Poreless Foundation", "category": "Makeup", "subcategory": "Foundation",
     "tags": "matte, poreless, natural finish", "search_keywords": "foundation face base coverage"},
    {"name": "Stay Quirky Liquid Foundation", "category": "Makeup", "subcategory": "Foundation",
     "tags": "liquid, medium coverage, dewy", "search_keywords": "foundation face base liquid"},

    # ── EYE SHADOW ─────────────────────────────────────────────────────────
    {"name": "Nykaa Matte to the Max Eye Shadow Palette", "category": "Makeup", "subcategory": "Eye Shadow",
     "tags": "matte, palette, 9 shades, everyday", "search_keywords": "eye shadow palette eyeshadow"},
    {"name": "Maybelline The Nudes Palette", "category": "Makeup", "subcategory": "Eye Shadow",
     "tags": "nude, shimmer, palette, 12 shades", "search_keywords": "eye shadow palette eyeshadow nude"},
    {"name": "Swiss Beauty Smoky Eye Shadow Palette", "category": "Makeup", "subcategory": "Eye Shadow",
     "tags": "smoky, glitter, bold, palette", "search_keywords": "eye shadow palette eyeshadow smoky"},

    # ── CONCEALER ──────────────────────────────────────────────────────────
    {"name": "Lakme 9to5 Weightless Mousse Concealer", "category": "Makeup", "subcategory": "Concealer",
     "tags": "mousse, weightless, full coverage", "search_keywords": "concealer face under eye dark circles"},
    {"name": "Maybelline Fit Me Concealer", "category": "Makeup", "subcategory": "Concealer",
     "tags": "natural finish, medium coverage, spf", "search_keywords": "concealer face blemish coverage"},

    # ── SHAMPOO ────────────────────────────────────────────────────────────
    {"name": "Pantene Silky Smooth Shampoo", "category": "Hair", "subcategory": "Shampoo",
     "tags": "silky, smooth, pro-v, damage repair", "search_keywords": "shampoo hair wash smooth frizz"},
    {"name": "Head & Shoulders Clean & Balanced Shampoo", "category": "Hair", "subcategory": "Shampoo",
     "tags": "dandruff, scalp care, anti-dandruff", "search_keywords": "shampoo hair dandruff scalp"},
    {"name": "Dove Intense Repair Shampoo", "category": "Hair", "subcategory": "Shampoo",
     "tags": "repair, keratin, damaged hair", "search_keywords": "shampoo hair repair damaged keratin"},
    {"name": "Mamaearth Onion Hair Fall Control Shampoo", "category": "Hair", "subcategory": "Shampoo",
     "tags": "onion, hair fall, biotin, nourishing", "search_keywords": "shampoo hair fall control growth"},
    {"name": "WOW Skin Science Apple Cider Vinegar Shampoo", "category": "Hair", "subcategory": "Shampoo",
     "tags": "apple cider vinegar, scalp balance, sulphate-free", "search_keywords": "shampoo hair clarifying scalp"},

    # ── CONDITIONER ────────────────────────────────────────────────────────
    {"name": "Pantene Daily Moisture Renewal Conditioner", "category": "Hair", "subcategory": "Conditioner",
     "tags": "moisture, daily, smooth, pro-v", "search_keywords": "conditioner hair smooth soft"},
    {"name": "Dove Intense Repair Conditioner", "category": "Hair", "subcategory": "Conditioner",
     "tags": "repair, keratin actives, deep nourish", "search_keywords": "conditioner hair repair deep"},
    {"name": "Mamaearth Onion Conditioner", "category": "Hair", "subcategory": "Conditioner",
     "tags": "onion, hair fall, soft, frizz-free", "search_keywords": "conditioner hair fall control"},

    # ── MEN'S GROOMING ─────────────────────────────────────────────────────
    {"name": "Nivea Men Dark Spot Reduction Face Wash", "category": "Skincare", "subcategory": "Face Wash",
     "tags": "men, dark spot, vitamin c, mud", "search_keywords": "men face wash cleanser skin"},
    {"name": "Beardo Charcoal Face Wash for Men", "category": "Skincare", "subcategory": "Face Wash",
     "tags": "men, charcoal, deep clean, oil control", "search_keywords": "men face wash cleanser charcoal"},
    {"name": "Nivea Men Original Moisture Face Cream", "category": "Skincare", "subcategory": "Moisturizer",
     "tags": "men, moisture, non-greasy, daily", "search_keywords": "men moisturizer face cream lotion"},
    {"name": "Bombay Shaving Company After Shave Lotion", "category": "Men's Grooming", "subcategory": "After Shave",
     "tags": "men, after shave, soothing, cooling", "search_keywords": "men after shave lotion grooming"},
]


class Command(BaseCommand):
    help = "Seed cosmetic products into the database"

    def add_arguments(self, parser):
        parser.add_argument(
            '--clear',
            action='store_true',
            help='Delete all existing products before seeding',
        )

    def handle(self, *args, **options):
        if options['clear']:
            count = Product.objects.count()
            Product.objects.all().delete()
            self.stdout.write(self.style.WARNING(f'Deleted {count} existing products.'))

        created = 0
        skipped = 0
        for data in PRODUCTS:
            _, is_new = Product.objects.get_or_create(
                name=data['name'],
                defaults={
                    'category': data.get('category', ''),
                    'subcategory': data.get('subcategory', ''),
                    'tags': data.get('tags', ''),
                    'search_keywords': data.get('search_keywords', ''),
                    'quantity': 0,
                }
            )
            if is_new:
                created += 1
            else:
                skipped += 1

        self.stdout.write(self.style.SUCCESS(
            f'Done. Created {created} products, skipped {skipped} already existing.'
        ))
