from playwright.sync_api import sync_playwright


def get_playwright_context(headless=True, proxy=None):

    pw = sync_playwright().start()

    browser = pw.chromium.launch(
        headless=headless,
        proxy=proxy,
        args=[
            "--disable-blink-features=AutomationControlled"
        ]
    )

    context = browser.new_context(

        user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120 Safari/537.36",

        viewport={"width":1280,"height":800},

        locale="en-GB"
    )

    return pw, browser, context