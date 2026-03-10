from scraping.playwright_driver import get_playwright_context
import os, json, re


class MotorsScraper:

    source_name = "Motors.co.uk"

    url = "https://www.motors.co.uk/search/cars/results/?damage-category=cat-n"

    def run(self, headless=False, proxy=None):

        pw, browser, context = get_playwright_context(headless=headless, proxy=proxy)

        page = context.new_page()

        try:

            print(f"[{self.source_name}] Opening page...")

            page.goto(self.url, timeout=60000)

            page.wait_for_load_state("domcontentloaded")

            # Accept cookies if shown
            for sel in [
                "button:has-text('Accept all')",
                "button:has-text('Accept')",
                "button:has-text('Agree')",
                "#onetrust-accept-btn-handler",
            ]:
                try:
                    page.click(sel, timeout=2000)
                    break
                except:
                    pass

            page.wait_for_timeout(2000)

            # Scroll to load all listings
            for _ in range(5):
                page.evaluate("window.scrollBy(0, document.body.scrollHeight)")
                page.wait_for_timeout(1000)

            # Save debug files
            os.makedirs("debug", exist_ok=True)
            open("debug/Motors.html", "w", encoding="utf-8").write(page.content())
            page.screenshot(path="debug/Motors.png", full_page=True)

            items = page.evaluate("""
                () => {
                    const listings = [];

                    const cards = document.querySelectorAll('article, [class*="listing-card"], [class*="vehicle-card"], [class*="search-result"]');

                    cards.forEach(card => {
                        const linkEl = card.querySelector('a[href*="/car-details/"], a[href*="/used-cars/"]');
                        if (!linkEl) return;

                        const rawHref = linkEl.href;
                        const href = rawHref.startsWith('http') ? rawHref : 'https://www.motors.co.uk' + rawHref;

                        const title = card.querySelector('h2, h3, [class*="title"], [class*="make"]')?.innerText?.trim();
                        if (!title) return;

                        const priceText = card.querySelector('[class*="price"], [class*="Price"]')?.innerText?.trim() || '';
                        const img = card.querySelector('img')?.src || '';
                        const location = card.querySelector('[class*="location"], [class*="dealer"], [class*="distance"]')?.innerText?.trim() || '';

                        listings.push({ title, link: href, price: priceText, img, location });
                    });

                    return listings;
                }
            """)

            print(f"[{self.source_name}] Raw items found:", len(items))

            listings = []

            for it in items:
                if not it.get("link"):
                    continue

                match_id = re.search(r'/(?:car-details|used-cars)/(\d+)', it["link"])
                external_id = match_id.group(1) if match_id else it["link"]

                price_str = it.get("price") or it.get("title") or ""
                match = re.search(r"£([\d,]+)", price_str)
                price_cleaned = float(match.group(1).replace(",", "")) if match else None

                listings.append({
                    "external_id": external_id,
                    "title": it["title"],
                    "description": "",
                    "price": price_cleaned,
                    "location": it.get("location", ""),
                    "listing_url": it["link"],
                    "image_urls": [it["img"]] if it.get("img") else [],
                })

            print(f"[{self.source_name}] Listings prepared:", len(listings))

            for i, l in enumerate(listings[:3]):
                print(f"Sample {i+1}:", json.dumps(l, ensure_ascii=False))

            return listings

        finally:
            context.close()
            browser.close()
            pw.stop()