import requests
from bs4 import BeautifulSoup


class GumtreeScraper:

    source_name = "Gumtree"

    def run(self):

        listings = []

        headers = {
            "User-Agent": "Mozilla/5.0"
        }

        for page in range(1, 5):

            url = f"https://www.gumtree.com/cars-vans-motorbikes/cars?q=cat+n&page={page}"

            r = requests.get(url, headers=headers)

            soup = BeautifulSoup(r.text, "html.parser")

            items = soup.select(".listing-maxi")

            for item in items:

                title = item.select_one("h2")
                link = item.select_one("a")
                price = item.select_one(".listing-price")
                img = item.select_one("img")

                if not title or not link:
                    continue

                listings.append({

                    "external_id": link["href"],

                    "title": title.text.strip(),

                    "description": "",

                    "price": price.text.strip() if price else "",

                    "location": "",

                    "listing_url": "https://www.gumtree.com" + link["href"],

                    "image_urls": [img["src"]] if img else [],

                })

        print(f"[Gumtree] Scraped {len(listings)} vehicles")

        return listings