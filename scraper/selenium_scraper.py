"""
Browser-rendered collection adapter.

Use this when a listing page requires JavaScript rendering. The collector
uses a standard Selenium Chrome session and does not attempt to bypass
CAPTCHAs, authentication, or other access controls.

Usage:
    python -m scraper.selenium_scraper "laptop" --pages 2
"""

import argparse
import logging
import random
import time

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

from scraper.config import BASE_URL, REQUEST_DELAY_SECONDS, REQUEST_DELAY_JITTER
from scraper.beautifulsoup_scraper import parse_listing_page
from scraper.schema import Product

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger(__name__)


def build_driver(headless: bool = True) -> webdriver.Chrome:
    """Create a standard Chrome driver for JavaScript-rendered pages."""
    options = Options()
    if headless:
        options.add_argument("--headless=new")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--window-size=1920,1080")
    return webdriver.Chrome(options=options)


def polite_delay() -> None:
    time.sleep(REQUEST_DELAY_SECONDS + random.uniform(0, REQUEST_DELAY_JITTER))


def scrape_search_query(query: str, pages: int = 1, headless: bool = True) -> list[Product]:
    """Collect rendered listing pages and parse product cards."""
    driver = build_driver(headless=headless)
    all_products: list[Product] = []

    try:
        for page in range(1, pages + 1):
            url = f"{BASE_URL}/catalog/?q={query.replace(' ', '+')}&page={page}"
            logger.info(f"Loading page {page}/{pages}: {url}")
            driver.get(url)

            try:
                WebDriverWait(driver, 15).until(
                    EC.presence_of_element_located(
                        (By.CSS_SELECTOR, "[data-qa-locator='general-products']")
                    )
                )
            except TimeoutException:
                logger.warning(
                    "Product grid did not appear. The layout may have changed or the site may "
                    "require interaction that this collector does not perform."
                )
                continue

            html = driver.page_source
            page_products = parse_listing_page(html, category=query)
            logger.info(f"Page {page}: parsed {len(page_products)} products")
            all_products.extend(page_products)

            if page < pages:
                polite_delay()

    finally:
        driver.quit()

    return all_products


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Collect rendered search listings with Selenium.")
    parser.add_argument("query", help="Search term, e.g. 'laptop'")
    parser.add_argument("--pages", type=int, default=1, help="Number of pages to collect")
    parser.add_argument("--no-headless", action="store_true", help="Show the browser window")
    args = parser.parse_args()

    results = scrape_search_query(args.query, pages=args.pages, headless=not args.no_headless)

    print(f"\nCollected {len(results)} total products for '{args.query}'.")
    for product in results[:5]:
        print(product.to_dict())
