from scraping.edge_driver import get_edge_driver
from selenium.webdriver.common.by import By
import time

class EbayScraper:
    source_name = "eBay"
    url = "https://www.ebay.co.uk/sch/i.html?_nkw=cat+n"

    def run(self):
        driver = get_edge_driver()
        driver.get(self.url)
        time.sleep(4)

        for _ in range(3):
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(2)

        items = driver.find_elements(By.CSS_SELECTOR, "div.s-item__wrapper")

        listings = []

        for item in items:
            try:
                title = item.find_element(By.CSS_SELECTOR, ".s-item__title").text
                link = item.find_element(By.CSS_SELECTOR, "a.s-item__link").get_attribute("href")
            except:
                continue

            try:
                price = item.find_element(By.CSS_SELECTOR, ".s-item__price").text
            except:
                price = None

            try:
                img = item.find_element(By.CSS_SELECTOR, "img.s-item__image-img").get_attribute("src")
            except:
                img = None

            listings.append({
                "external_id": link,
                "title": title,
                "description": "",
                "price": price,
                "location": "",
                "listing_url": link,
                "image_urls": [img] if img else [],
            })

        driver.quit()
        return listings
