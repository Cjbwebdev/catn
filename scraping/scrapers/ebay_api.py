import requests
from bs4 import BeautifulSoup
import os


class EbayScraper:

    source_name = "eBay"

    def run(self):

        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/120 Safari/537.36"
        }

        url = "https://www.ebay.co.uk/sch/i.html?_nkw=cat+n+car"

        r = requests.get(url, headers=headers)

        os.makedirs("debug", exist_ok=True)

        with open("debug/ebay.html", "w", encoding="utf-8") as f:
            f.write(r.text)

        print("Saved debug/ebay.html")

        soup = BeautifulSoup(r.text, "html.parser")

        items = soup.select("li.s-item")

        print("Items found:", len(items))

        listings = []

        for item in items:

            title = item.select_one(".s-item__title")
            link = item.select_one(".s-item__link")
            price = item.select_one(".s-item__price")
            img = item.select_one(".s-item__image-img")

            if not title or not link:
                continue

            listings.append({
                "external_id": link["href"],
                "title": title.text.strip(),
                "description": "",
                "price": price.text if price else "",
                "location": "",
                "listing_url": link["href"],
                "image_urls": [img["src"]] if img else [],
            })

        print(f"[eBay] Scraped {len(listings)} vehicles")

        return listings