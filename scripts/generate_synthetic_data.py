"""
Synthetic data generator — DEMO ONLY, not real scraped data.

Purpose: let the database, EDA, ML, and dashboard be built and run
end-to-end independently of live collection.

Usage:
    python -m scripts.generate_synthetic_data
"""

import random
from datetime import datetime, timedelta

from database.database import init_db, upsert_products

CATEGORIES = {
    "laptop": ["Dell", "HP", "Lenovo", "Asus", "Apple"],
    "mobile": ["Samsung", "Xiaomi", "Infinix", "Realme", "Apple"],
    "headphones": ["JBL", "Sony", "Anker", "Boat", "Apple"],
}

random.seed(42)


def _fake_url(name: str, idx: int) -> str:
    slug = name.lower().replace(" ", "-")
    return f"https://www.daraz.pk/products/{slug}-i{100000 + idx}.html"


def generate(num_products: int = 40, days_of_history: int = 21) -> list[dict]:
    records = []
    start_date = datetime.utcnow() - timedelta(days=days_of_history)

    for i in range(num_products):
        category = random.choice(list(CATEGORIES.keys()))
        brand = random.choice(CATEGORIES[category])
        base_price = random.uniform(15000, 350000)
        name = f"{brand} {category.title()} Model {i+1}"
        url = _fake_url(name, i)
        rating = round(random.uniform(3.2, 5.0), 1)
        num_reviews = random.randint(5, 3000)

        price = base_price
        for day in range(days_of_history):
            drift = random.uniform(-0.015, 0.008)
            price = max(price * (1 + drift), base_price * 0.6)
            original_price = round(price * random.uniform(1.0, 1.3), 2)
            discount_percent = round((original_price - price) / original_price * 100, 1)

            scraped_at = (start_date + timedelta(days=day)).isoformat()

            records.append({
                "product_name": name,
                "category": category,
                "brand": brand,
                "price": round(price, 2),
                "original_price": original_price,
                "discount_percent": discount_percent,
                "rating": rating,
                "num_reviews": num_reviews,
                "availability": "in_stock",
                "seller": f"{brand} Official Store",
                "product_url": url,
                "scraped_at": scraped_at,
            })

    return records


if __name__ == "__main__":
    init_db()
    records = generate()
    count = upsert_products(records)
    print(f"Generated and inserted {count} price_history rows "
          f"across {len(set(r['product_url'] for r in records))} synthetic products.")
    print("This is DEMO data — replace with live data when appropriate.")
