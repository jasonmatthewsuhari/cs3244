# README

## Dataset Acquisition

Instead of scraping tweets ourselves, we opted to use a preprocessed version of the dataset from [this repository](https://github.com/RussellDash332/CS3244-Twemoji/blob/main/Datasets), which contains only text and emoji labels. This dataset is from four years ago and does not include additional metadata, models, or preprocessing pipelines. We obtained permission from the owner to use this dataset.

## Why We Chose This Approach

Initially, we explored multiple avenues for acquiring the dataset, including using the Twitter v2 API and scraping via Nitter. However, both approaches proved impractical due to the following reasons:

### Twitter v2 API Limitations:
- Extremely restrictive rate limits (~100 requests/month), far below the 12M tweets required for our dataset.

### Nitter Scraping Issues:
- **Slow Scraping Speed** – Nitter retrieved tweets at ~3 seconds per tweet, requiring over a year to process the dataset without parallelization.
- **Frequent Downtime** – Public Nitter instances often went down or became unreliable.
- **Self-Hosting Challenges** – Our self-hosted Nitter instance was unstable, frequently going offline.
- **Increased Rate Limiting** – After Elon Musk’s acquisition of Twitter, the platform implemented stricter anti-scraping measures, further limiting data retrieval.

## Final Decision
Given these constraints, we opted to use an older, pre-scraped version of the dataset as the most viable solution for our project.

