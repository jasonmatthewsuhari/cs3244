from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup

# useful tweet ids for testing
# working: 741592336031846400
# tnf: 744009997806354432
# with replies and reply: 747643690521341953
# (inappropriate, but image) 746900975928090628

def fetch_html_playwright(tweet_id):
    url = f"https://nitter.net/username/status/{tweet_id}"

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)  # Run in headless mode
        page = browser.new_page()

        # Disable images, CSS, and fonts
        page.route("**/*", lambda route: route.abort() if route.request.resource_type in ["image", "stylesheet", "font"] else route.continue_())

        try:
            page.goto(url, timeout=10000, wait_until="domcontentloaded")
            
            html = page.content()
            soup = BeautifulSoup(html, "lxml")  # Use lxml for faster parsing

            print(soup.prettify())

            if not soup.select_one("div.tweet-content"):
                return None  # Tweet not found

            # **Extract Main Tweet**
            tweet_text = soup.select_one("div.tweet-content").text.strip()
            tweet_image = None
            image_tag = soup.select_one("div.attachments a.still-image")
            if image_tag:
                tweet_image = f"https://nitter.net{image_tag['href']}"
            author_name = soup.select_one("div.fullname-and-username a.fullname").text.strip()
            username = soup.select_one("div.fullname-and-username a.username").text.strip()
            tweet_time = soup.select_one("span.tweet-date a").text.strip()
            tweet_id = soup.select_one("link[rel=canonical]")["href"].split("/")[-1]

            # Extract stats (Replies, Retweets, Quotes, Likes)
            stats = [
                soup.select_one(f"div.tweet-stats span:nth-of-type({i})").text.strip()
                if soup.select_one(f"div.tweet-stats span:nth-of-type({i})") else "0"
                for i in range(1, 5)
            ]
            reply_count, retweets, quotes, likes = map(lambda x: int(x) if x.isdigit() else 0, stats)

            quoted_tweet = None
            quoted_section = soup.select_one("div.quote")
            if quoted_section:
                quoted_author = quoted_section.select_one("div.fullname-and-username a.fullname").text.strip()
                quoted_username = quoted_section.select_one("div.fullname-and-username a.username").text.strip()
                quoted_text = quoted_section.select_one("div.quote-text").text.strip()
                quoted_time = quoted_section.select_one("span.tweet-date a").text.strip()
                quoted_id = quoted_section.select_one("a.quote-link")["href"].split("/")[-1]

                quoted_tweet = {
                    "tweet_id": quoted_id,
                    "author_name": quoted_author,
                    "username": quoted_username,
                    "tweet_text": quoted_text,
                    "tweet_time": quoted_time
                }

            replies = []
            reply_elements = soup.select(".replies .tweet-body")

            for reply in reply_elements:
                reply_user = reply.select_one(".fullname").text.strip() if reply.select_one(".fullname") else None
                reply_handle = reply.select_one(".username").text.strip() if reply.select_one(".username") else None
                reply_text = reply.select_one(".tweet-content").text.strip() if reply.select_one(".tweet-content") else None
                reply_date = reply.select_one(".tweet-date a").text.strip() if reply.select_one(".tweet-date a") else None

                replies.append({
                    "username": reply_user,
                    "handle": reply_handle,
                    "reply_text": reply_text,
                    "reply_date": reply_date
                })

            tweet_data = {
                "tweet_id": tweet_id,
                "tweet_text": tweet_text,
                "tweet_image": tweet_image,
                "author_name": author_name,
                "username": username,
                "tweet_time": tweet_time,
                "reply_count": reply_count,
                "retweets": retweets,
                "quotes": quotes,
                "likes": likes,
                "quoted_tweet": quoted_tweet,
                "replies": replies
            }

            browser.close()
            return tweet_data

        except Exception as e:
            print(f"Error fetching tweet {tweet_id}: {e}")
            return None

if __name__ == "__main__":
    tweet_id = "747643690521341953"
    result = fetch_html_playwright(tweet_id)
    print(result)
