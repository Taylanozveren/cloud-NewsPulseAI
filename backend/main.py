import os
import requests
from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
from typing import Optional
from datetime import datetime

load_dotenv()

SEARCH_ENDPOINT = os.getenv("SEARCH_ENDPOINT")
SEARCH_KEY      = os.getenv("SEARCH_KEY")

INDEX_NAME  = "azureblob-index"
API_VERSION = "2023-07-01-Preview"

app = FastAPI(
    title="NewsPulseAI Search API",
    description="Search and filter news articles indexed from Azure Blob Storage.",
    version="1.3.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# ──────────────────────────────────────────────────────────
# 🔎 Generic Azure Search helper
# ──────────────────────────────────────────────────────────
def azure_search(
    query: str = "*",
    top: int = 25,
    filters: Optional[str] = None,
    orderby: Optional[str] = None,
):
    url = f"{SEARCH_ENDPOINT}/indexes/{INDEX_NAME}/docs/search?api-version={API_VERSION}"
    headers = {
        "Content-Type": "application/json",
        "api-key": SEARCH_KEY,
    }
    payload: dict = {"search": query, "top": top}
    if filters:
        payload["filter"] = filters
    if orderby:
        payload["orderby"] = orderby

    resp = requests.post(url, headers=headers, json=payload)
    resp.raise_for_status()
    return resp.json().get("value", [])

# ──────────────────────────────────────────────────────────
# 📄 Endpoints
# ──────────────────────────────────────────────────────────
@app.get("/news", summary="List all news (latest first)", tags=["News"])
def get_news(top: int = 25):
    docs = azure_search(top=top, orderby="content/published desc")
    return [
        {
            "title":       d["content"]["title"],
            "source":      d["content"]["source"],
            "date":        d["content"]["published"],
            "sentiment":   d["content"]["sentiment"],
            "summary":     d["content"]["summary"],
            "url":         d["content"]["url"],
            "keyphrases":  d["content"]["keyphrases"],
            "category":    d["content"].get("category", "general"),
        }
        for d in docs
    ]


@app.get("/search", summary="Search news by keyword", tags=["News"])
def search_news(q: str = Query(..., description="Search query"), top: int = 10):
    docs = azure_search(query=q, top=top, orderby="content/published desc")
    return [
        {
            "title":       d["content"]["title"],
            "source":      d["content"]["source"],
            "date":        d["content"]["published"],
            "sentiment":   d["content"]["sentiment"],
            "summary":     d["content"]["summary"],
            "url":         d["content"]["url"],
            "keyphrases":  d["content"]["keyphrases"],
            "category":    d["content"].get("category", "general"),
        }
        for d in docs
    ]


@app.get("/sentiment", summary="Filter news by sentiment", tags=["News"])
def sentiment_news(
    type: str = Query("positive", enum=["positive", "neutral", "negative"]),
    top: int = 20,
):
    flt  = f"content/sentiment eq '{type}'"
    docs = azure_search(top=top, filters=flt, orderby="content/published desc")
    return [
        {
            "title":       d["content"]["title"],
            "source":      d["content"]["source"],
            "date":        d["content"]["published"],
            "sentiment":   d["content"]["sentiment"],
            "summary":     d["content"]["summary"],
            "url":         d["content"]["url"],
            "keyphrases":  d["content"]["keyphrases"],
            "category":    d["content"].get("category", "general"),
        }
        for d in docs
    ]


@app.get("/date", summary="Filter news by date range (ISO8601)", tags=["News"])
def date_news(start: str, end: str, top: int = 20):
    flt  = f"content/published ge '{start}' and content/published le '{end}'"
    docs = azure_search(top=top, filters=flt, orderby="content/published desc")
    return [
        {
            "title":       d["content"]["title"],
            "source":      d["content"]["source"],
            "date":        d["content"]["published"],
            "sentiment":   d["content"]["sentiment"],
            "summary":     d["content"]["summary"],
            "url":         d["content"]["url"],
            "keyphrases":  d["content"]["keyphrases"],
            "category":    d["content"].get("category", "general"),
        }
        for d in docs
    ]


@app.get("/keyphrase", summary="Filter news by keyphrase", tags=["News"])
def keyphrase_news(kw: str, top: int = 20):
    docs = azure_search(query=kw, top=top, orderby="content/published desc")
    return [
        {
            "title":       d["content"]["title"],
            "source":      d["content"]["source"],
            "date":        d["content"]["published"],
            "sentiment":   d["content"]["sentiment"],
            "summary":     d["content"]["summary"],
            "url":         d["content"]["url"],
            "keyphrases":  d["content"]["keyphrases"],
            "category":    d["content"].get("category", "general"),
        }
        for d in docs
    ]


@app.get("/category", summary="Filter news by category", tags=["News"])
def category_news(category: str = Query(...), top: int = 20):
    flt  = f"content/category eq '{category}'"
    docs = azure_search(top=top, filters=flt, orderby="content/published desc")
    return [
        {
            "title":       d["content"]["title"],
            "source":      d["content"]["source"],
            "date":        d["content"]["published"],
            "sentiment":   d["content"]["sentiment"],
            "summary":     d["content"]["summary"],
            "url":         d["content"]["url"],
            "keyphrases":  d["content"]["keyphrases"],
            "category":    d["content"].get("category", "general"),
        }
        for d in docs
    ]


@app.get("/news/{id}", summary="Get news by ID (URL)", tags=["News"])
def get_news_by_id(id: str):
    docs = azure_search(query=id, top=1)
    if not docs:
        return {"error": "Not found"}
    d = docs[0]
    return {
        "title":      d["content"]["title"],
        "source":     d["content"]["source"],
        "date":       d["content"]["published"],
        "sentiment":  d["content"]["sentiment"],
        "summary":    d["content"]["summary"],
        "url":        d["content"]["url"],
        "keyphrases": d["content"]["keyphrases"],
        "category":   d["content"].get("category", "general"),
    }


@app.get("/stats", summary="Basic sentiment stats", tags=["Stats"])
def sentiment_stats():
    docs = azure_search(top=100)
    from collections import Counter
    sentiments = [d["content"].get("sentiment", "-") for d in docs]
    return dict(Counter(sentiments))

# ──────────────────────────────────────────────────────────
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
