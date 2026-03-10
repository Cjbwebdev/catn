# scraping/edge_driver.py
from selenium import webdriver
from selenium.webdriver.edge.options import Options

def get_edge_driver(headless: bool = False, window_size: tuple = (1366, 900)):
    options = Options()
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument(
        "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36"
    )

    if headless:
        options.add_argument("--headless=new")

    driver = webdriver.Edge(options=options)
    driver.set_window_size(window_size[0], window_size[1])
    driver.set_page_load_timeout(40)
    return driver
