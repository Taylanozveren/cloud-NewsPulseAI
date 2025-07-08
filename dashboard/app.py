import streamlit as st
import requests
from collections import Counter
import plotly.express as px
import pandas as pd

# ─────────────────────────────────────────────────────────────────────────────
# 🎨 Optimized CSS
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 10px;
        margin-bottom: 2rem;
        color: white;
        text-align: center;
    }
    
    .main-header h1 {
        font-size: 2.5rem;
        margin-bottom: 0.5rem;
        font-weight: 700;
    }
    
    .main-header p {
        font-size: 1.1rem;
        opacity: 0.9;
    }
    
    .article-card {
        background: white;
        border: 1px solid #e9ecef;
        border-radius: 12px;
        padding: 1.5rem;
        margin: 1rem 0;
        box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        transition: transform 0.2s ease;
    }
    
    .article-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 16px rgba(0,0,0,0.15);
    }
    
    .article-title {
        font-size: 1.3rem;
        font-weight: 600;
        color: #2c3e50;
        margin-bottom: 0.8rem;
        line-height: 1.4;
    }
    
    .article-meta {
        display: flex;
        gap: 1rem;
        margin-bottom: 1rem;
        font-size: 0.9rem;
        color: #6c757d;
    }
    
    .sentiment-badge {
        display: inline-block;
        padding: 0.25rem 0.75rem;
        border-radius: 20px;
        font-size: 0.8rem;
        font-weight: 500;
        margin-right: 0.5rem;
    }
    
    .sentiment-positive { background: #d4edda; color: #155724; }
    .sentiment-negative { background: #f8d7da; color: #721c24; }
    .sentiment-neutral { background: #e2e3e5; color: #383d41; }
    
    .keyphrases {
        background: #f8f9fa;
        padding: 0.75rem;
        border-radius: 8px;
        margin-top: 1rem;
        border-left: 3px solid #667eea;
    }
    
    .keyphrase-tag {
        display: inline-block;
        background: #667eea;
        color: white;
        padding: 0.2rem 0.6rem;
        border-radius: 15px;
        font-size: 0.8rem;
        margin: 0.2rem 0.3rem 0.2rem 0;
    }
    
    .stat-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 1.5rem;
        border-radius: 10px;
        text-align: center;
    }
    
    .stat-number {
        font-size: 2rem;
        font-weight: 700;
        margin-bottom: 0.5rem;
    }
    
    .stat-label {
        font-size: 0.9rem;
        opacity: 0.9;
    }
    
    .read-more-btn {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 0.5rem 1rem;
        border-radius: 20px;
        text-decoration: none;
        font-weight: 500;
        font-size: 0.9rem;
        display: inline-block;
        margin-top: 1rem;
        transition: all 0.3s ease;
    }
    
    .read-more-btn:hover {
        transform: translateY(-1px);
        box-shadow: 0 4px 12px rgba(102, 126, 234, 0.4);
    }
    
    .no-results {
        text-align: center;
        padding: 3rem;
        color: #6c757d;
    }
    
    .about-section {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 1.5rem;
        border-radius: 10px;
        margin-bottom: 2rem;
    }
    
    .about-section h3 {
        margin-bottom: 1rem;
        font-size: 1.2rem;
    }
    
    .about-section p {
        margin-bottom: 0.5rem;
        opacity: 0.9;
    }
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────────────────────
# 🛠️ Configuration
st.set_page_config(
    page_title="NewsPulseAI", 
    page_icon="📰",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ─────────────────────────────────────────────────────────────────────────────
# 🎯 Header
st.markdown("""
<div class="main-header">
    <h1>📰 NewsPulseAI</h1>
    <p>AI-Powered News Analytics & Summarization Platform</p>
</div>
""", unsafe_allow_html=True)

# About section - more visible
st.markdown("""
<div class="about-section">
    <h3>ℹ️ About This Platform</h3>
    <p><strong>Developed by:</strong> Taylan Özveren</p>
    <p><strong>Technologies:</strong> Storage Container & Azure AI Language & AI Search & Azure OpenAI • FastAPI • Streamlit</p>
    <p><strong>Features:</strong> Summarization • Sentiment Analysis • Keyphrase Extraction • Category Filtering</p>
</div>
""", unsafe_allow_html=True)

API_BASE = "http://localhost:8000"

# ─────────────────────────────────────────────────────────────────────────────
# 🎨 Sidebar
st.sidebar.header("🔍 Search & Filters")

keyword = st.sidebar.text_input("🔎 Search Keywords", placeholder="Enter keywords...")
sentiment = st.sidebar.selectbox("😊 Sentiment Filter", ["All", "positive", "neutral", "negative"])
category = st.sidebar.selectbox("📂 Category Filter", ["All", "technology", "science", "business"])
count = st.sidebar.slider("📊 Articles to Display", 5, 50, 20)

# ─────────────────────────────────────────────────────────────────────────────
# 🔗 API Functions
@st.cache_data(ttl=300)
def call_api(path, params=None):
    try:
        r = requests.get(f"{API_BASE}{path}", params=params, timeout=10)
        r.raise_for_status()
        return r.json()
    except requests.exceptions.ConnectionError:
        st.error("🔌 Cannot connect to API. Please ensure the backend is running on http://localhost:8000")
        return []
    except requests.exceptions.Timeout:
        st.error("⏱️ Request timed out. Please try again.")
        return []
    except Exception as e:
        st.error(f"❌ API error: {str(e)}")
        return []

# ─────────────────────────────────────────────────────────────────────────────
# 📊 Load Data
with st.spinner("Loading news articles..."):
    if category != "All":
        news = call_api("/category", {"category": category, "top": count})
    elif keyword:
        news = call_api("/search", {"q": keyword, "top": count})
    elif sentiment != "All":
        news = call_api("/sentiment", {"type": sentiment, "top": count})
    else:
        news = call_api("/news", {"top": count})

# ─────────────────────────────────────────────────────────────────────────────
# 📈 Statistics
if news:
    sentiments = [a["sentiment"] for a in news if a.get("sentiment")]
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown(f"""
        <div class="stat-card">
            <div class="stat-number">{len(news)}</div>
            <div class="stat-label">Total Articles</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        positive_count = sentiments.count("positive")
        st.markdown(f"""
        <div class="stat-card">
            <div class="stat-number">{positive_count}</div>
            <div class="stat-label">Positive</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        sources = len(set(a["source"] for a in news))
        st.markdown(f"""
        <div class="stat-card">
            <div class="stat-number">{sources}</div>
            <div class="stat-label">Sources</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        avg_keyphrases = round(sum(len(a["keyphrases"]) for a in news) / len(news), 1)
        st.markdown(f"""
        <div class="stat-card">
            <div class="stat-number">{avg_keyphrases}</div>
            <div class="stat-label">Avg Keyphrases</div>
        </div>
        """, unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────────────────────
# 📰 Articles
if news:
    st.markdown("## 📰 Latest Articles")
    
    for art in news:
        sentiment_class = f"sentiment-{art['sentiment']}" if art.get('sentiment') else "sentiment-neutral"
        
        st.markdown(f"""
        <div class="article-card">
            <div class="article-title">{art['title']}</div>
            <div class="article-meta">
                <span>📰 <strong>{art['source']}</strong></span>
                <span>📅 {art['date'][:10]}</span>
                <span>📂 {art.get('category', 'general').title()}</span>
            </div>
            <div class="sentiment-badge {sentiment_class}">
                {art['sentiment'].title() if art.get('sentiment') else 'Neutral'}
            </div>
            <p style="margin-top: 1rem; line-height: 1.6; color: #495057;">{art["summary"]}</p>
            <a href="{art['url']}" target="_blank" class="read-more-btn">📖 Read Full Article</a>
        </div>
        """, unsafe_allow_html=True)
        
        if art.get("keyphrases"):
            keyphrase_tags = "".join([f'<span class="keyphrase-tag">{kp}</span>' for kp in art["keyphrases"]])
            st.markdown(f"""
            <div class="keyphrases">
                <div style="font-size: 0.9rem; font-weight: 600; color: #495057; margin-bottom: 0.5rem;">🏷️ Key Phrases:</div>
                {keyphrase_tags}
            </div>
            """, unsafe_allow_html=True)

else:
    st.markdown("""
    <div class="no-results">
        <div style="font-size: 3rem; margin-bottom: 1rem;">🔍</div>
        <h3>No articles found</h3>
        <p>Try adjusting your filters or check if the backend is running.</p>
    </div>
    """, unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────────────────────
# 📊 Visualizations
if news:
    st.markdown("## 📊 Analytics Dashboard")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### Sentiment Distribution")
        sentiment_counts = Counter([a["sentiment"] for a in news if a.get("sentiment")])
        if sentiment_counts:
            fig = px.pie(
                values=list(sentiment_counts.values()),
                names=list(sentiment_counts.keys()),
                color_discrete_map={
                    'positive': '#28a745',
                    'negative': '#dc3545',
                    'neutral': '#6c757d'
                }
            )
            fig.update_traces(textposition='inside', textinfo='percent+label')
            fig.update_layout(showlegend=True, height=400, font=dict(size=12))
            st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.markdown("### Category Distribution")
        category_counts = Counter([a.get("category", "general") for a in news])
        if category_counts:
            fig = px.bar(
                x=list(category_counts.keys()),
                y=list(category_counts.values()),
                color=list(category_counts.values()),
                color_continuous_scale='Blues'
            )
            fig.update_layout(
                xaxis_title="Categories",
                yaxis_title="Article Count",
                showlegend=False,
                height=400
            )
            st.plotly_chart(fig, use_container_width=True)

# ─────────────────────────────────────────────────────────────────────────────
# 📱 Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; padding: 2rem; color: #6c757d;">
    <p>© 2025 NewsPulseAI — Powered by Azure AI Services</p>
    <p style="font-size: 0.9rem;">FastAPI • Streamlit • Azure AI Language & Search</p>
</div>
""", unsafe_allow_html=True)