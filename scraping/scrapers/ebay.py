from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import time


class EbayScraper:

    source_name = "eBay"
    start_url = "https://www.ebay.co.uk/sch/i.html?_nkw=cat+n+car"

    def get_driver(self):
        options = Options()
        options.add_argument("--headless=new")
        options.add_argument("--disable-gpu")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("user-agent=Mozilla/5.0")

        driver = webdriver.Chrome(
            service=Service(ChromeDriverManager().install()),
            options=options
        )
        return driver

    def run(self):
        driver = self.get_driver()
        driver.get(self.start_url)

        # Allow JS to load
        time.sleep(3)

        # Scroll to load lazy items
        for _ in range(3):
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(2)

        items = driver.find_elements(By.CSS_SELECTOR, "li.s-item")

        listings = []

        for item in items:
            try:
                title_el = item.find_element(By.CSS_SELECTOR, ".s-item__title")
                link_el = item.find_element(By.CSS_SELECTOR, ".s-item__link")
            except:
                continue

            title = title_el.text.strip()
            link = link_el.get_attribute("href")

            # Price
            try:
                price_el = item.find_element(By.CSS_SELECTOR, ".s-item__price")
                price = price_el.text.strip()
            except:
                price = None

            # Image
            try:
                img_el = item.find_element(By.CSS_SELECTOR, "img")
                img_url = img_el.get_attribute("src")
            except:
                img_url = None

            listings.append({
                "external_id": link,
                "title": title,
                "description": "",
                "price": price,
                "location": "",
                "listing_url": link,
                "image_urls": [img_url] if img_url else [],
            })

        driver.quit()
        return listings
