# ingest_news.py

import os
import json
import uuid
from datetime import datetime, timedelta, timezone
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

from datetime import datetime, timedelta, timezone

from datetime import datetime, timedelta

def fetch_articles():
    # Son 24 saatteki en güncel haberleri al
    resp = newsapi.get_top_headlines(
        language="en",
        page_size=30,
        # optionally country="us" or category="technology"
    )
    print("NewsAPI raw response:", resp.get("totalResults"), "articles")
    return [a for a in resp.get("articles", []) if a.get("content")]



def enrich(article: dict) -> dict:
    text = article["title"] + ". " + (article.get("content") or "")
    poller = lang_client.begin_analyze_actions(
        [text],
        actions=[ExtractiveSummaryAction(max_sentence_count=3)]
    )

    summary = ""
    # 2 katmanlı döngü: action_result (ilk katman), document_result (ikinci katman)
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
        "url": article["url"]
    }


def upload_news_article(doc: dict):
    blob_name = f"{uuid.uuid4()}.json"
    data = json.dumps(doc, ensure_ascii=False).encode("utf-8")
    container_client.upload_blob(blob_name, data, overwrite=True)
    print(f"Uploaded: {blob_name}")

def main():
    print("Fetching articles…")
    arts = fetch_articles()
    print(f"Found {len(arts)} articles, enriching…")
    for art in arts:
        enriched = enrich(art)
        upload_news_article(enriched)
    print("Done.")

if __name__ == "__main__":
    main()
