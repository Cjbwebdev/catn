import requests
import xml.etree.ElementTree as ET


class GumtreeScraper:

    source_name = "Gumtree"

    url = "https://www.gumtree.com/search?search_category=cars&search_location=uk&q=cat+n&format=rss"

    def run(self):

        listings = []

        headers = {
            "User-Agent": "Mozilla/5.0"
        }

        try:

            r = requests.get(self.url, headers=headers, timeout=30)

            # Check if response is XML
            if not r.text.strip().startswith("<?xml"):
                print("[Gumtree] Response was not RSS/XML")
                print(r.text[:200])
                return listings

            root = ET.fromstring(r.text)

        except Exception as e:

            print("[Gumtree] RSS parsing failed:", e)
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

        print(f"[Gumtree] Scraped {len(listings)} vehicles")

        return listings