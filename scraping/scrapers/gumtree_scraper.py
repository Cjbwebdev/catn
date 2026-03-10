import re, sys
from playwright.sync_api import sync_playwright

class GumtreeScraper:
    source_name = "Gumtree"
    base_url = "https://www.gumtree.com/cars/cat-n?page={page}"

    def run(self, headless=True, max_pages=5):
        print(f"[{self.source_name}] Opening page...")
        listings = []

        with sync_playwright() as pw:
            browser = pw.chromium.launch(headless=headless)
            context = browser.new_context()
            page = context.new_page()

            for page_num in range(1, max_pages + 1):
                url = self.base_url.format(page=page_num)
                print(f"[{self.source_name}] Fetching page {page_num}...")
                page.goto(url, timeout=60000)
                page.wait_for_timeout(2000)  # small wait to render content

                items = page.evaluate("""
                () => {
                    const nodes = Array.from(document.querySelectorAll('[data-q="tile"]'));
                    return nodes.map(n => {
                        const link = n.querySelector('a')?.href;
                        const title = n.innerText.trim();
                        const img = n.querySelector('img')?.src;
                        const price = n.querySelector('span[data-q="price"]')?.innerText;
                        return {link, title, img, price};
                    }).filter(x => x.link);
                }
                """)

                print(f"[{self.source_name}] Raw items found: {len(items)}")

                for item in items:
                    # Clean price - fall back to extracting from title if selector returns None
                    price_str = item.get("price") or item.get("title") or ""
                    match = re.search(r"£([\d,]+)", price_str)
                    price_cleaned = float(match.group(1).replace(",", "")) if match else None

                    # Clean title
                    title_cleaned = " ".join(item["title"].splitlines())

                    listings.append({
                        "external_id": item["link"],
                        "title": title_cleaned,
                        "description": "",
                        "price": price_cleaned,
                        "location": "",
                        "listing_url": item["link"],
                        "image_urls": [item["img"]] if item["img"] else [],
                    })

                if not items:
                    print(f"[{self.source_name}] No more items found on page {page_num}. Stopping pagination.")
                    break

            context.close()
            browser.close()

        print(f"[{self.source_name}] Listings prepared: {len(listings)}")
        return listings