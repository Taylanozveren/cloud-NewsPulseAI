import os
import requests
from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
from typing import List, Optional
from datetime import datetime

load_dotenv()

SEARCH_ENDPOINT = os.getenv("SEARCH_ENDPOINT")
SEARCH_KEY = os.getenv("SEARCH_KEY")
INDEX_NAME = "azureblob-index"
API_VERSION = "2023-07-01-Preview"

app = FastAPI(
    title="NewsPulseAI Search API",
    description="Search and filter news articles indexed from Azure Blob Storage.",
    version="1.1.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], allow_methods=["*"], allow_headers=["*"]
)

def azure_search(query: str = "*", top: int = 25, filters: Optional[str] = None):
    url = f"{SEARCH_ENDPOINT}/indexes/{INDEX_NAME}/docs/search?api-version={API_VERSION}"
    headers = {"Content-Type": "application/json", "api-key": SEARCH_KEY}
    data = {"search": query, "top": top}
    if filters:
        data["filter"] = filters
    r = requests.post(url, headers=headers, json=data)
    return r.json().get("value", [])

@app.get("/news", summary="List all news", tags=["News"])
def get_news(top: int = 25):
    docs = azure_search(top=top)
    return [
        {
            "title": d.get("content", {}).get("title"),
            "source": d.get("content", {}).get("source"),
            "date": d.get("content", {}).get("published"),
            "sentiment": d.get("content", {}).get("sentiment"),
            "summary": d.get("content", {}).get("summary"),
            "url": d.get("content", {}).get("url"),
            "keyphrases": d.get("content", {}).get("keyphrases", []),
        }
        for d in docs
    ]

@app.get("/search", summary="Search news by keyword", tags=["News"])
def search_news(q: str = Query(..., description="Search query"), top: int = 10):
    docs = azure_search(query=q, top=top)
    return [
        {
            "title": d.get("content", {}).get("title"),
            "source": d.get("content", {}).get("source"),
            "date": d.get("content", {}).get("published"),
            "sentiment": d.get("content", {}).get("sentiment"),
            "summary": d.get("content", {}).get("summary"),
            "url": d.get("content", {}).get("url"),
            "keyphrases": d.get("content", {}).get("keyphrases", []),
        }
        for d in docs
    ]

@app.get("/sentiment", summary="Filter news by sentiment", tags=["News"])
def sentiment_news(type: str = Query("positive", enum=["positive", "neutral", "negative"]), top: int = 20):
    # Azure Search filter syntax: content/sentiment eq 'positive'
    filter_str = f"content/sentiment eq '{type}'"
    docs = azure_search(top=top, filters=filter_str)
    return [
        {
            "title": d.get("content", {}).get("title"),
            "source": d.get("content", {}).get("source"),
            "date": d.get("content", {}).get("published"),
            "sentiment": d.get("content", {}).get("sentiment"),
            "summary": d.get("content", {}).get("summary"),
            "url": d.get("content", {}).get("url"),
            "keyphrases": d.get("content", {}).get("keyphrases", []),
        }
        for d in docs
    ]

@app.get("/date", summary="Filter news by date range (ISO8601)", tags=["News"])
def date_news(start: str, end: str, top: int = 20):
    # ISO8601 örn: 2025-07-01T00:00:00Z
    filter_str = f"content/published ge '{start}' and content/published le '{end}'"
    docs = azure_search(top=top, filters=filter_str)
    return [
        {
            "title": d.get("content", {}).get("title"),
            "source": d.get("content", {}).get("source"),
            "date": d.get("content", {}).get("published"),
            "sentiment": d.get("content", {}).get("sentiment"),
            "summary": d.get("content", {}).get("summary"),
            "url": d.get("content", {}).get("url"),
            "keyphrases": d.get("content", {}).get("keyphrases", []),
        }
        for d in docs
    ]

@app.get("/keyphrase", summary="Filter news by keyphrase", tags=["News"])
def keyphrase_news(kw: str, top: int = 20):
    # Basit anahtar kelime ile search (keyphrase alanında filtrelenemez, Azure’da string araması ile yapılır)
    docs = azure_search(query=kw, top=top)
    return [
        {
            "title": d.get("content", {}).get("title"),
            "source": d.get("content", {}).get("source"),
            "date": d.get("content", {}).get("published"),
            "sentiment": d.get("content", {}).get("sentiment"),
            "summary": d.get("content", {}).get("summary"),
            "url": d.get("content", {}).get("url"),
            "keyphrases": d.get("content", {}).get("keyphrases", []),
        }
        for d in docs
    ]

@app.get("/news/{id}", summary="Get news by ID (URL)", tags=["News"])
def get_news_by_id(id: str):
    # id burada URL olacak (newsapi json id=article url)
    docs = azure_search(query=id, top=1)
    if not docs:
        return {"error": "Not found"}
    d = docs[0]
    return {
        "title": d.get("content", {}).get("title"),
        "source": d.get("content", {}).get("source"),
        "date": d.get("content", {}).get("published"),
        "sentiment": d.get("content", {}).get("sentiment"),
        "summary": d.get("content", {}).get("summary"),
        "url": d.get("content", {}).get("url"),
        "keyphrases": d.get("content", {}).get("keyphrases", []),
    }

@app.get("/stats", summary="Basic sentiment stats", tags=["Stats"])
def sentiment_stats():
    # Hepsini çekip (ilk 100), sentiment istatistiği dön.
    docs = azure_search(top=100)
    from collections import Counter
    sentiments = [d.get("content", {}).get("sentiment", "-") for d in docs]
    counter = Counter(sentiments)
    return dict(counter)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
