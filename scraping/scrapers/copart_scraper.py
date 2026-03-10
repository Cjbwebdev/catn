import re, sys, requests

class CopartScraper:
    source_name = "Copart"
    base_url = "https://www.copart.co.uk/public/lots/search"

    def run(self, max_pages=5):
        print(f"[{self.source_name}] Fetching pages...")
        listings = []

        headers = {
            "Accept": "application/json, text/javascript, */*; q=0.01",
            "User-Agent": "Mozilla/5.0"
        }

        for page_num in range(1, max_pages + 1):
            params = {
                "query": "Cat N",
                "page": page_num,
                "pageSize": 100,
            }
            try:
                r = requests.get(self.base_url, params=params, headers=headers, timeout=20)
                r.raise_for_status()
                data = r.json()
            except Exception as e:
                print(f"[{self.source_name}] Request exception: {e}")
                break

            vehicles = data.get("results", [])
            if not vehicles:
                print(f"[{self.source_name}] No more vehicles on page {page_num}")
                break

            for v in vehicles:
                price = None
                if v.get("bidPrice"):
                    try:
                        price = float(v["bidPrice"].replace(",", ""))
                    except:
                        price = None

                listings.append({
                    "external_id": f"{self.source_name}-{v.get('id')}",
                    "title": v.get("lotName") or "",
                    "description": v.get("lotDescription") or "",
                    "price": price,
                    "location": v.get("location") or "",
                    "listing_url": f"https://www.copart.co.uk/lot/{v.get('id')}" if v.get("id") else "",
                    "image_urls": [v.get("imageUrl")] if v.get("imageUrl") else [],
                })

        print(f"[{self.source_name}] Listings scraped: {len(listings)}")
        return listings