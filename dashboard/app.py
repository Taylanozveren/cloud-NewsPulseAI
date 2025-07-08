import streamlit as st
import requests
from datetime import datetime
from collections import Counter
import matplotlib.pyplot as plt

API_BASE = "http://localhost:8000"

st.set_page_config(page_title="NewsPulseAI", layout="wide")
st.title("📰 NewsPulseAI Demo Dashboard")

st.sidebar.header("🔎 Search & Filter")
search_query = st.sidebar.text_input("Keyword Search", value="")
sentiment = st.sidebar.selectbox(
    "Sentiment Filter", options=["All", "positive", "neutral", "negative", "mixed"]
)
top_n = st.sidebar.slider("How many news to show?", 5, 50, 20)

# API call helpers with error handling
def get_news(top):
    try:
        r = requests.get(f"{API_BASE}/news", params={"top": top}, timeout=5)
        if r.ok:
            return r.json()
    except Exception as e:
        st.error(f"API connection error: {e}")
    return []

def search_news(q, top):
    try:
        r = requests.get(f"{API_BASE}/search", params={"q": q, "top": top}, timeout=5)
        if r.ok:
            return r.json()
    except Exception as e:
        st.error(f"API connection error: {e}")
    return []

def filter_by_sentiment(type, top):
    try:
        r = requests.get(f"{API_BASE}/sentiment", params={"type": type, "top": top}, timeout=5)
        if r.ok:
            return r.json()
    except Exception as e:
        st.error(f"API connection error: {e}")
    return []

# Data loading
news = []
if search_query:
    news = search_news(search_query, top_n)
elif sentiment != "All":
    news = filter_by_sentiment(sentiment, top_n)
else:
    news = get_news(top_n)

# Main news feed
if news:
    st.success(f"Found {len(news)} news articles.")
    for n in news:
        st.markdown(
            f"### {n['title']}\n"
            f"**Source:** `{n['source']}` &nbsp;|&nbsp; "
            f"**Date:** {n['date'][:10]} &nbsp;|&nbsp; "
            f"**Sentiment:** :{n['sentiment']}:"
        )
        st.write(n["summary"])
        st.markdown(f"[Read more...]({n['url']})", unsafe_allow_html=True)
        st.caption("**Keyphrases:** " + ", ".join(n["keyphrases"]))
        st.divider()
else:
    st.info("No news found! Make sure your backend is running and indexed data is available.")

# Sentiment Pie Chart
if news:
    sentiments = [n["sentiment"] for n in news if n["sentiment"]]
    if sentiments:
        st.write("### Sentiment Distribution")
        counter = Counter(sentiments)
        fig, ax = plt.subplots()
        ax.pie(counter.values(), labels=counter.keys(), autopct='%1.1f%%')
        st.pyplot(fig)
    else:
        st.info("No sentiment data available.")

st.markdown("---")
st.caption("Made with Azure AI + FastAPI + Streamlit | NewsPulseAI")
