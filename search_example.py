import os
import requests
from datetime import datetime

endpoint = os.getenv("SEARCH_ENDPOINT")
key = os.getenv("SEARCH_KEY")
index_name = "azureblob-index"

url = f"{endpoint}/indexes/{index_name}/docs/search?api-version=2023-07-01-Preview"
headers = {
    "Content-Type": "application/json",
    "api-key": key,
}

# Fetch all news
all_data = {
    "search": "*",
    "top": 50   # Adjust as needed
}
resp = requests.post(url, headers=headers, json=all_data)
all_results = resp.json().get("value", [])

def pretty_datetime(dt):
    try:
        return datetime.fromisoformat(dt.replace("Z", "+00:00")).strftime("%Y-%m-%d %H:%M")
    except Exception:
        return dt

if not all_results:
    print("No news found!")
else:
    print(f"\nAll {len(all_results)} news articles:\n")
    for i, r in enumerate(all_results, 1):
        content = r.get("content", {})
        print(f"--- Article {i} ---")
        print("Source      :", content.get("source", "-"))
        print("Title       :", content.get("title", "-"))
        print("Date        :", pretty_datetime(content.get("published", "-")))
        print("Sentiment   :", content.get("sentiment", "-"))
        print("Keyphrases  :", ", ".join(content.get("keyphrases", [])))
        print("Summary     :", content.get("summary", "-"))
        print("URL         :", content.get("url", "-"))
        print("Search Score:", r.get("@search.score", "-"))
        print()

    print("\n==== News articles containing 'trump' (in title, summary, or keyphrases) ====\n")
    trump_news = []
    for i, r in enumerate(all_results, 1):
        content = r.get("content", {})
        text_all = (
            content.get("title", "") +
            content.get("summary", "") +
            " ".join(content.get("keyphrases", []))
        ).lower()
        if "trump" in text_all:
            trump_news.append((i, content, r.get("@search.score", "-")))

    if not trump_news:
        print("No news articles mentioning 'trump'.")
    else:
        for idx, content, score in trump_news:
            print(f"--- Article {idx} ---")
            print("Source      :", content.get("source", "-"))
            print("Title       :", content.get("title", "-"))
            print("Date        :", pretty_datetime(content.get("published", "-")))
            print("Sentiment   :", content.get("sentiment", "-"))
            print("Keyphrases  :", ", ".join(content.get("keyphrases", [])))
            print("Summary     :", content.get("summary", "-"))
            print("URL         :", content.get("url", "-"))
            print("Search Score:", score)
            print()
