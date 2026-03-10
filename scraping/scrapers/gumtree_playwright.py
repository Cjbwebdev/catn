from scraping.playwright_driver import get_playwright_context
import os, json, sys
import re

class GumtreeScraper:

    source_name = "Gumtree"

    url = "https://www.gumtree.com/search?search_category=cars&search_location=uk&q=cat+n"

    def run(self, headless=False, proxy=None):

        pw, browser, context = get_playwright_context(headless=headless, proxy=proxy)

        page = context.new_page()

        try:

            print(f"[{self.source_name}] Opening page...")

            page.goto(self.url, timeout=60000)

            page.wait_for_load_state("domcontentloaded")

            # Accept cookies if shown
            for sel in [
                "button:has-text('Accept')",
                "button:has-text('Agree')",
                "button:has-text('Allow')"
            ]:
                try:
                    page.click(sel, timeout=2000)
                    break
                except:
                    pass

            # Scroll page to load listings
            for _ in range(10):
                page.evaluate("window.scrollBy(0, document.body.scrollHeight)")
                page.wait_for_timeout(1000)

            # Save debug files
            os.makedirs("debug", exist_ok=True)

            html = page.content()

            open("debug/Gumtree.html", "w", encoding="utf-8").write(html)

            page.screenshot(path="debug/Gumtree.png", full_page=True)

            # Extract listings
            items = page.evaluate("""
                () => {

                    const listings = [];

                    const links = document.querySelectorAll("a[href*='/p/']");

                    links.forEach(link => {

                        const card = link.closest("div");
                        if(!card) return;

                        const title = link.innerText.trim();
                        const href = link.href;

                        const priceEl = card.querySelector("span");
                        let price = priceEl ? priceEl.innerText.trim() : "";

                        // extract number from price text
                        if(price){
                            const match = price.match(/[0-9,]+/);
                            price = match ? match[0].replace(/,/g,"") : "";
                        }

                        const img = card.querySelector("img")?.src;

                        listings.push({
                            title:title,
                            link:href,
                            price:price,
                            img:img
                        });

                    });

                    return listings;

                }
                """)

            print(f"[{self.source_name}] Raw items found:", len(items))

            listings = []

            for it in items:

                if not it["link"]:
                    continue

                listings.append({
                    "external_id": it["link"],
                    "title": it["title"],
                    "description": "",
                    "price": float(re.search(r"£([\d,]+)", it.get("price") or it.get("title") or "").group(1).replace(",","")) if re.search(r"£([\d,]+)", it.get("price") or it.get("title") or "") else None,
                    "location": "",
                    "listing_url": it["link"],
                    "image_urls": [it["img"]] if it["img"] else [],
                })

            print(f"[{self.source_name}] Listings prepared:", len(listings))

            # show sample
            for i,l in enumerate(listings[:3]):
                print(f"Sample {i+1}:", json.dumps(l, ensure_ascii=False))

            return listings

        finally:

            context.close()
            browser.close()
            pw.stop()