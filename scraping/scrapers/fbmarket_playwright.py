from scraping.playwright_driver import get_playwright_context
import os, json, sys

class FBMarketplaceScraper:
    source_name = "FBMarketplace"
    url = "https://www.facebook.com/marketplace/uk/search/?query=cat%20n"

    def run(self, headless=False, proxy=None):
        pw, browser, context = get_playwright_context(headless=headless, proxy=proxy)
        page = context.new_page()
        try:
            page.goto(self.url, timeout=60000)
            page.wait_for_load_state("networkidle")

            # Scroll to load listings
            for _ in range(6):
                page.evaluate("window.scrollBy(0, window.innerHeight);")
                page.wait_for_timeout(1000)

            os.makedirs("debug", exist_ok=True)
            html = page.content()
            page.screenshot(path=f"debug/{self.source_name}.png", full_page=True)
            open(f"debug/{self.source_name}.html", "w", encoding="utf-8").write(html)

            # Extract listings
            items = page.evaluate("""
            () => {
                const nodes = Array.from(document.querySelectorAll('[role="article"]'));
                return nodes.map(n => {
                    const title = n.querySelector('span')?.innerText.trim();
                    const link = n.querySelector('a')?.href;
                    const price = n.querySelector('span[aria-label*="£"]')?.innerText.trim();
                    const img = n.querySelector('img')?.src;
                    return {title, link, price, img};
                }).filter(x => x.title && x.link);
            }
            """)

            print(f"[{self.source_name}] Found {len(items)} items.", file=sys.stdout)
            listings = []
            for it in items:
                listings.append({
                    "external_id": it["link"],
                    "title": it["title"],
                    "description": "",
                    "price": it["price"],
                    "location": "",
                    "listing_url": it["link"],
                    "image_urls": [it["img"]] if it.get("img") else [],
                })

            for i, l in enumerate(listings[:3]):
                print(f"[{self.source_name}] sample {i+1}: {json.dumps(l, ensure_ascii=False)}", file=sys.stdout)

            return listings

        finally:
            context.close()
            browser.close()
            pw.stop()