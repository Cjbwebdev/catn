from selenium import webdriver
from selenium.webdriver.edge.options import Options

def get_edge_driver():
    options = Options()
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument("user-agent=Mozilla/5.0")

    # Debug mode: see the browser
    # options.add_argument("--headless=new")

    driver = webdriver.Edge(options=options)
    return driver
