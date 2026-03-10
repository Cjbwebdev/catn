import requests
import xml.etree.ElementTree as ET


class EbayScraper:

    source_name = "eBay"

    url = "https://www.ebay.co.uk/sch/i.html?_nkw=cat+n+car&_rss=1"

    def run(self):

        listings = []

        headers = {
            "User-Agent": "Mozilla/5.0"
        }

        r = requests.get(self.url, headers=headers)

        # Check if response looks like XML
        if not r.text.strip().startswith("<?xml"):
            print("[eBay] Response was not RSS/XML")
            print(r.text[:200])
            return listings

        try:
            root = ET.fromstring(r.text)
        except Exception as e:
            print("[eBay] XML parse failed:", e)
            return listings

        for item in root.findall(".//item"):

            title = item.findtext("title")
            link = item.findtext("link")
            description = item.findtext("description")

            if not link:
                continue

            listings.append({
                "external_id": link,
                "title": title or "",
                "description": description or "",
                "price": "",
                "location": "",
                "listing_url": link,
                "image_urls": [],
            })

        print(f"[eBay] Scraped {len(listings)} vehicles")

        return listings