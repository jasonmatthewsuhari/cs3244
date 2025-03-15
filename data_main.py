import json
import os
from scripts.pw_scrape import fetch_html_playwright  # Importing function

# make sure to change the input file to the correct one, whichever one that is
INPUT_FILE = "data/dog.txt"
OUTPUT_FILE = "data/output/tweets_data.json"
FAILURES_FILE = "data/output/failures.txt"

def process_tweets():
    tweets_data = {}

    os.makedirs(os.path.dirname(OUTPUT_FILE), exist_ok=True)
    if os.path.exists(OUTPUT_FILE):
        with open(OUTPUT_FILE, "r", encoding="utf-8") as file:
            try:
                tweets_data = json.load(file)
            except json.JSONDecodeError:
                tweets_data = {}

    with open(INPUT_FILE, "r", encoding="utf-8") as file:
        total_tweets = sum(1 for _ in file) - 1  # Subtract 1 for header

    processed = 0
    failures = 0

    with open(INPUT_FILE, "r", encoding="utf-8") as file:
        next(file)  # Skip header line

        for line in file:
            processed += 1
            progress_pct = (processed / total_tweets) * 100
            
            parts = line.strip().split("\t")
            if len(parts) < 1:
                failures += 1
                continue 

            tweet_id = parts[0]
            html_string = fetch_html_playwright(tweet_id)

            if not html_string:  # aka if the tweet is not found
                failures += 1
                failure_rate = (failures / processed) * 100
                print(f"❌ Failed Tweet ID: {tweet_id} @ [{processed}/{total_tweets}] - {progress_pct:.1f}% done, {failure_rate:.1f}% failure rate")
                with open(FAILURES_FILE, "a", encoding="utf-8") as f:
                    f.write(f"{tweet_id}\n")
                continue

            tweets_data[tweet_id] = html_string

            with open(OUTPUT_FILE, "w", encoding="utf-8") as json_file:
                json.dump(tweets_data, json_file, indent=4, ensure_ascii=False)

            failure_rate = (failures / processed) * 100
            print(f"✅ Processed Tweet ID: {tweet_id} @ [{processed}/{total_tweets}] - {progress_pct:.1f}% done, {failure_rate:.1f}% failure rate")

    final_failure_rate = (failures / total_tweets) * 100
    print(f"\nProcessing complete!")
    print(f"Total tweets processed: {total_tweets}")
    print(f"Total failures: {failures}")
    print(f"Final failure rate: {final_failure_rate:.1f}%")
    print(f"Failed tweet IDs have been logged to {FAILURES_FILE}")

# **Run the script**
if __name__ == "__main__":
    process_tweets()
