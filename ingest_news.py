import os
import json
import base64
from dotenv import load_dotenv
from newsapi import NewsApiClient
from azure.core.credentials import AzureKeyCredential
from azure.ai.textanalytics import TextAnalyticsClient, ExtractiveSummaryAction
from azure.storage.blob import BlobServiceClient

load_dotenv()

newsapi = NewsApiClient(api_key=os.getenv("NEWSAPI_KEY"))

lang_client = TextAnalyticsClient(
    endpoint=os.getenv("LANG_ENDPOINT"),
    credential=AzureKeyCredential(os.getenv("LANG_KEY"))
)

blob_service = BlobServiceClient.from_connection_string(
    os.getenv("STORAGE_CONN_STR")
)
container_client = blob_service.get_container_client(
    os.getenv("BLOB_CONTAINER")
)

CATEGORIES = ["technology", "science", "business"]  # Dilediğini ekle/çıkar

def fetch_articles_with_category(category):
    resp = newsapi.get_top_headlines(
        language="en",
        category=category,
        page_size=15
    )
    return [
        {**a, "category": category}
        for a in resp.get("articles", [])
        if a.get("content")
    ]

def enrich(article: dict) -> dict:
    text = article["title"] + ". " + (article.get("content") or "")
    poller = lang_client.begin_analyze_actions(
        [text],
        actions=[ExtractiveSummaryAction(max_sentence_count=3)]
    )

    summary = ""
    action_results = poller.result()
    for action_result in action_results:
        for document_result in action_result:
            if not document_result.is_error:
                summary = " ".join([s.text for s in document_result.sentences])

    sentiment = lang_client.analyze_sentiment([text])[0].sentiment
    keyphrases = lang_client.extract_key_phrases([text])[0].key_phrases

    return {
        "id": article["url"],
        "title": article["title"],
        "published": article["publishedAt"],
        "summary": summary,
        "sentiment": sentiment,
        "keyphrases": keyphrases,
        "source": article["source"]["name"],
        "url": article["url"],
        "category": article.get("category", "general")
    }

def url_to_blobname(url):
    # Unique: url'yi base64 ile encode et, Windows'a uyumlu!
    return base64.urlsafe_b64encode(url.encode("utf-8")).decode("ascii") + ".json"

def upload_news_article(doc: dict):
    blob_name = url_to_blobname(doc["url"])
    data = json.dumps(doc, ensure_ascii=False).encode("utf-8")
    container_client.upload_blob(blob_name, data, overwrite=True)  # overwrite=True: Günceller!
    print(f"Uploaded/Updated: {blob_name}")

def main():
    print("Fetching articles by category…")
    all_arts = []
    for cat in CATEGORIES:
        arts = fetch_articles_with_category(cat)
        all_arts.extend(arts)
        print(f"Found {len(arts)} articles in category: {cat}")

    print(f"Total {len(all_arts)} articles, enriching…")
    for art in all_arts:
        enriched = enrich(art)
        upload_news_article(enriched)
    print("Done.")

if __name__ == "__main__":
    main()
