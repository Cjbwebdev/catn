from bs4 import BeautifulSoup
from scraping.edge_driver import get_edge_driver
import time

class GumtreeScraper:
    source_name = "Gumtree"
    url = "https://www.gumtree.com/cars/uk?query=cat+n"

    def run(self):
        driver = get_edge_driver()
        driver.get(self.url)
        time.sleep(3)

        html = driver.page_source
        driver.quit()

        soup = BeautifulSoup(html, "lxml")
        items = soup.select("article.listing-maxi")

        listings = []

        for item in items:
            title_el = item.select_one("h2.listing-title")
            link_el = item.select_one("a.listing-link")
            price_el = item.select_one(".listing-price")
            img_el = item.select_one("img")

            if not title_el or not link_el:
                continue

            listings.append({
                "external_id": "https://www.gumtree.com" + link_el["href"],
                "title": title_el.get_text(strip=True),
                "description": "",
                "price": price_el.get_text(strip=True) if price_el else None,
                "location": "",
                "listing_url": "https://www.gumtree.com" + link_el["href"],
                "image_urls": [img_el.get("src")] if img_el else [],
            })

        return listings
