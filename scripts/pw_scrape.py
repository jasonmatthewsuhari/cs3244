from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup

#working: 741592336031846400
#tnf: 744009997806354432
#with replies and reply: 747643690521341953

def fetch_html_playwright(tweet_id):
    url = f"https://nitter.net/username/status/{tweet_id}"

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()
        page.goto(url, timeout=10000)
        
        html = page.content()
        soup = BeautifulSoup(html, "html.parser")
        # print(soup.prettify())

        if not soup.select_one("div.tweet-content"):
            return None # this means the tweet is not found for whatever rzn

        tweet_text = soup.select_one("div.tweet-content").text.strip()
        author_name = soup.select_one("div.fullname-and-username a.fullname").text
        username = soup.select_one("div.fullname-and-username a.username").text
        tweet_time = soup.select_one("span.tweet-date a").text
        tweet_id = soup.select_one("link[rel=canonical]").text
        stats = [soup.select_one(f"div.tweet-stats span:nth-of-type({i})").text.strip() if soup.select_one(f"div.tweet-stats span:nth-of-type({i})") else "0" for i in range(1, 5)]
        replies, retweets, quotes, likes = stats

        return {
            "tweet_id": tweet_id,
            "tweet_text": tweet_text,
            "author_name": author_name,
            "username": username,
            "tweet_time": tweet_time,
            "replies": int(replies) if replies else 0,
            "retweets": int(retweets) if retweets else 0,
            "quotes": int(quotes) if quotes else 0,
            "likes": int(likes) if likes else 0
        }

        browser.close()

if __name__ == "__main__":
    x = fetch_html_playwright("742550426269143040")
    print(x)
