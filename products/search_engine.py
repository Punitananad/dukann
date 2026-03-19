"""
RackFinder Smart Search Engine
================================
Handles query normalization, synonym expansion, multi-token scoring,
and fuzzy matching via rapidfuzz.
"""

import re
from rapidfuzz import fuzz

# ---------------------------------------------------------------------------
# Synonym dictionary — map common misspellings/variants to canonical terms
# ---------------------------------------------------------------------------
SYNONYMS: dict[str, str] = {
    # Face
    "facewash": "face wash",
    "facewashh": "face wash",
    "fash wash": "face wash",
    "facewahs": "face wash",
    "cleanser": "face wash",
    "cleaner": "face wash",
    "foaming": "face wash",

    # Moisturizer
    "moisturiser": "moisturizer",
    "moisturizr": "moisturizer",
    "moisterizer": "moisturizer",
    "moistuizer": "moisturizer",
    "cream": "moisturizer",
    "lotion": "moisturizer",

    # Lipstick / lip
    "lipstik": "lipstick",
    "lipstck": "lipstick",
    "lip color": "lipstick",
    "lip colour": "lipstick",

    # Eyeliner
    "eyelinr": "eyeliner",
    "eye liner": "eyeliner",
    "kajal": "eyeliner",

    # Mascara
    "mascra": "mascara",
    "masacara": "mascara",

    # Foundation
    "foundaton": "foundation",
    "foundtion": "foundation",
    "foundat": "foundation",

    # Eye shadow
    "eyeshadow": "eye shadow",
    "eye shaow": "eye shadow",

    # Concealer
    "conceler": "concealer",
    "concelar": "concealer",

    # Sunscreen
    "sunscren": "sunscreen",
    "sunblock": "sunscreen",
    "spf": "sunscreen",

    # Serum
    "srum": "serum",

    # Toner
    "tonner": "toner",

    # Gender
    "mens": "men",
    "men's": "men",
    "womens": "women",
    "women's": "women",

    # Hair
    "shampoo": "shampoo",
    "shampo": "shampoo",
    "condtioner": "conditioner",
    "conditoner": "conditioner",
}


def normalize(query: str) -> str:
    """Lowercase, strip, collapse whitespace, remove special chars."""
    query = query.lower().strip()
    query = re.sub(r"[^a-z0-9 ]", " ", query)
    query = re.sub(r"\s+", " ", query).strip()
    return query


def apply_synonyms(query: str) -> str:
    """
    Replace known misspellings / shorthand with canonical terms.
    Checks two-word phrases first, then single words.
    """
    words = query.split()
    result: list[str] = []
    i = 0
    while i < len(words):
        # Try two-word match first
        if i + 1 < len(words):
            bigram = f"{words[i]} {words[i + 1]}"
            if bigram in SYNONYMS:
                result.append(SYNONYMS[bigram])
                i += 2
                continue
        result.append(SYNONYMS.get(words[i], words[i]))
        i += 1
    return " ".join(result)


def split_query(query: str) -> list[str]:
    """Return individual meaningful tokens (length > 1)."""
    return [t for t in query.split() if len(t) > 1]


# ---------------------------------------------------------------------------
# Scoring
# ---------------------------------------------------------------------------

def _score_field(token: str, field: str, weight: int) -> int:
    """Return weight if token is a substring of field, else 0."""
    return weight if token in field else 0


def score_product(product, query: str, tokens: list[str]) -> int:
    """
    Calculate relevance score for a single product.

    Scoring tiers:
      +50  exact query in name
      +30  exact query in subcategory
      +20  exact query in tags / search_keywords
      +15  exact query in category
      +10  exact query in brand

    Per-token bonuses (applied for each token):
      +15  token in name
      +10  token in subcategory / tags / keywords
      +5   token in category / brand

    Fuzzy boost (rapidfuzz):
      +40  partial_ratio(query, name) ≥ 85
      +25  partial_ratio(query, name) ≥ 70
      +10  partial_ratio(query, name) ≥ 55
      +15  partial_ratio(query, subcategory or category) ≥ 80
    """
    name = (product.name or "").lower()
    brand = (product.brand or "").lower()
    category = (product.category or "").lower()
    subcat = (product.subcategory or "").lower()
    tags = (product.tags or "").lower()
    keywords = (product.search_keywords or "").lower()

    score = 0

    # ── Full-query exact substring matches ─────────────────────────────────
    score += _score_field(query, name, 50)
    score += _score_field(query, subcat, 30)
    score += _score_field(query, tags, 20)
    score += _score_field(query, keywords, 20)
    score += _score_field(query, category, 15)
    score += _score_field(query, brand, 10)

    # ── Per-token substring matches ─────────────────────────────────────────
    for token in tokens:
        score += _score_field(token, name, 15)
        score += _score_field(token, subcat, 10)
        score += _score_field(token, tags, 10)
        score += _score_field(token, keywords, 10)
        score += _score_field(token, category, 5)
        score += _score_field(token, brand, 5)

    # ── Fuzzy matching ──────────────────────────────────────────────────────
    name_ratio = fuzz.partial_ratio(query, name)
    if name_ratio >= 85:
        score += 40
    elif name_ratio >= 70:
        score += 25
    elif name_ratio >= 55:
        score += 10

    # Fuzzy on category / subcategory
    cat_str = f"{subcat} {category}".strip()
    cat_ratio = fuzz.partial_ratio(query, cat_str)
    if cat_ratio >= 80:
        score += 15
    elif cat_ratio >= 65:
        score += 7

    # Fuzzy on tags + keywords blob
    tag_blob = f"{tags} {keywords}".strip()
    if tag_blob:
        tag_ratio = fuzz.partial_ratio(query, tag_blob)
        if tag_ratio >= 80:
            score += 10

    return score


# ---------------------------------------------------------------------------
# Main entry point
# ---------------------------------------------------------------------------

def smart_search(products, raw_query: str, top_n: int = 15) -> list:
    """
    Full search pipeline:
      normalize → synonym expand → tokenize → score → rank → slice

    Returns up to `top_n` products, sorted by score descending.
    Returns empty list when score is 0 for all (no match at all).
    """
    query = normalize(raw_query)
    query = apply_synonyms(query)
    tokens = split_query(query)

    scored: list[tuple[int, object]] = []
    for product in products:
        s = score_product(product, query, tokens)
        if s > 0:
            scored.append((s, product))

    scored.sort(key=lambda x: x[0], reverse=True)
    return [p for _, p in scored[:top_n]]


def fallback_fuzzy(products, raw_query: str, top_n: int = 8) -> list:
    """
    Last-resort fuzzy pass when smart_search returns nothing.
    Uses token_sort_ratio for more forgiving full-name matching.
    """
    query = normalize(raw_query)
    scored: list[tuple[int, object]] = []
    for product in products:
        name = (product.name or "").lower()
        ratio = fuzz.token_sort_ratio(query, name)
        if ratio >= 45:
            scored.append((ratio, product))
    scored.sort(key=lambda x: x[0], reverse=True)
    return [p for _, p in scored[:top_n]]
