from playwright.sync_api import sync_playwright

def fetch_html_playwright(url):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()
        page.goto(url, timeout=10000)
        print(page.content())
        browser.close()

fetch_html_playwright("https://nitter.net/username/status/744009997806354432")
