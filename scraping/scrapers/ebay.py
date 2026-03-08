from bs4 import BeautifulSoup
from .base import BaseScraper


class EbayScraper(BaseScraper):

    source_name = "eBay"

    start_url = "https://www.ebay.co.uk/sch/i.html?_nkw=cat+n+cars"

    def parse(self, html):

        soup = BeautifulSoup(html, "html.parser")

        listings = []

        for item in soup.select(".s-item"):

            title = item.select_one(".s-item__title")

            if not title:
                continue

            listings.append({
                "external_id": title.text,
                "title": title.text,
                "price": None,
                "description": "",
                "location": "",
                "listing_url": "",
                "image_urls": [],
            })

        return listings