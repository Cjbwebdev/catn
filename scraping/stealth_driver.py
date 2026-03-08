import undetected_chromedriver as uc

def get_stealth_driver():
    options = uc.ChromeOptions()
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-gpu")
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument("user-agent=Mozilla/5.0")

    driver = uc.Chrome(options=options)
    driver.set_page_load_timeout(30)
    return driver
