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

# Burada anlamlı bir arama terimi gir (ör: trump, musk, economy, election, school vs.)
query = "trump"
data = {
    "search": query,
    "top": 5
}
resp = requests.post(url, headers=headers, json=data)
results = resp.json().get("value", [])

if not results:
    print("No news found for:", query)
else:
    print(f"\nTop {len(results)} results for search: '{query}'\n")
    for i, r in enumerate(results, 1):
        content = r.get("content", {})
        print(f"--- Article {i} ---")
        print("Source  :", content.get("source", "-"))
        print("Title   :", content.get("title", "-"))
        # Tarihi daha okunabilir göster
        date_str = content.get("published", "-")
        try:
            date_str = datetime.fromisoformat(date_str.replace("Z", "+00:00")).strftime("%d.%m.%Y %H:%M")
        except Exception:
            pass
        print("Date    :", date_str)
        print("Summary :", content.get("summary", "-"))
        print("Sentiment:", content.get("sentiment", "-"))
        print("Keyphrases:", ", ".join(content.get("keyphrases", [])))
        print("URL     :", content.get("url", "-"))
        print()

