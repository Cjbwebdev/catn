import requests
import json
from scraping.services import save_listings
from listings.models import SourceSite
import sys
import os

class CopartAPIScraper:
    source_name = "Copart"
    base_url = "https://www.copart.com/public/lots/search"

    # Query parameters for Cat N vehicles in the UK
    params = {
        "query": "cat n",
        "searchType": "lot",
        "filter": "catn",  # Copart internal Cat N filter
        "sort": "lotdate",  # sort by most recent
        "page": 1,
        "size": 100  # max per page
    }

    def fetch_page(self, page: int = 1):
        self.params["page"] = page
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                          "AppleWebKit/537.36 (KHTML, like Gecko) "
                          "Chrome/117.0.0.0 Safari/537.36",
            "Accept": "application/json, text/plain, */*",
        }

        try:
            r = requests.get(self.base_url, params=self.params, headers=headers, timeout=30)
            r.raise_for_status()
            data = r.json()
            return data
        except requests.HTTPError as e:
            print(f"[{self.source_name}] HTTP error: {e}")
        except requests.RequestException as e:
            print(f"[{self.source_name}] Request exception: {e}")
        except json.JSONDecodeError:
            print(f"[{self.source_name}] Failed to parse JSON")
        return None

    def run(self):
        listings = []
        page = 1
        while True:
            print(f"[{self.source_name}] Fetching page {page}...")
            data = self.fetch_page(page)
            if not data or "lots" not in data or len(data["lots"]) == 0:
                print(f"[{self.source_name}] No more vehicles on page {page}")
                break

            for lot in data["lots"]:
                title = lot.get("lotDescription", "").strip()
                link = f"https://www.copart.com/lot/{lot.get('lotNumber')}"
                price = lot.get("currentBid") or lot.get("estimatedPrice")
                img_url = lot.get("thumbnailUrl")
                location = lot.get("location", "")

                listings.append({
                    "external_id": link,
                    "title": title,
                    "description": lot.get("subTitle", ""),
                    "price": price,
                    "location": location,
                    "listing_url": link,
                    "image_urls": [img_url] if img_url else [],
                })

            page += 1

        print(f"[{self.source_name}] Scraped {len(listings)} vehicles")
        return listings