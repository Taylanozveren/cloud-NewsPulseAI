import streamlit as st
import requests
from collections import Counter
import plotly.express as px
import pandas as pd
import math

# ─────────────────────────────────────────────────────────────────────────────
# 🎨 Tema Yöneticisi
def get_theme_css(dark_mode=False):
    if dark_mode:
        return """
        <style>
            .stApp {
                background-color: #0e1117;
                color: #fafafa;
            }
            .main-header {
                background: linear-gradient(135deg, #1f2937 0%, #374151 100%);
                padding: 2rem;
                border-radius: 10px;
                margin-bottom: 2rem;
                color: white;
                text-align: center;
            }
            .article-card {
                background: #1f2937;
                border: 1px solid #374151;
                border-radius: 12px;
                padding: 1.5rem;
                margin: 1rem 0;
                box-shadow: 0 2px 8px rgba(0,0,0,0.3);
                transition: transform 0.2s ease;
            }
            .article-card:hover {
                transform: translateY(-2px);
                box-shadow: 0 4px 16px rgba(0,0,0,0.4);
            }
            .article-title {
                color: #e5e7eb;
            }
            .stat-card {
                background: linear-gradient(135deg, #374151 0%, #4b5563 100%);
                color: white;
                padding: 1.5rem;
                border-radius: 10px;
                text-align: center;
            }
            .about-section {
                background: linear-gradient(135deg, #374151 0%, #4b5563 100%);
                color: white;
                padding: 1.5rem;
                border-radius: 10px;
                margin-bottom: 2rem;
            }
            .keyphrases {
                background: #374151;
                border-left: 3px solid #6b7280;
            }
            .pagination-container {
                background: #1f2937;
                border: 1px solid #374151;
            }
            .search-suggestion {
                background: #374151;
                border: 1px solid #4b5563;
                color: #e5e7eb;
            }
            .search-suggestion:hover {
                background: #4b5563;
            }
        </style>
        """
    else:
        return """
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
                flex-wrap: wrap;
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
            
            .pagination-container {
                background: white;
                border: 1px solid #e9ecef;
                border-radius: 10px;
                padding: 1rem;
                margin: 2rem 0;
                display: flex;
                justify-content: space-between;
                align-items: center;
                flex-wrap: wrap;
                gap: 1rem;
            }
            
            .pagination-info {
                color: #6c757d;
                font-size: 0.9rem;
            }
            
            .pagination-buttons {
                display: flex;
                gap: 0.5rem;
                flex-wrap: wrap;
            }
            
            .pagination-btn {
                padding: 0.5rem 1rem;
                background: #667eea;
                color: white;
                border: none;
                border-radius: 5px;
                cursor: pointer;
                font-size: 0.9rem;
                transition: background 0.2s;
            }
            
            .pagination-btn:hover {
                background: #5a6fd8;
            }
            
            .pagination-btn:disabled {
                background: #ccc;
                cursor: not-allowed;
            }
            
            .search-suggestions {
                position: relative;
                margin-bottom: 1rem;
            }
            
            .search-suggestion {
                background: white;
                border: 1px solid #e9ecef;
                padding: 0.5rem 1rem;
                cursor: pointer;
                border-radius: 5px;
                margin: 0.2rem 0;
                transition: background 0.2s;
            }
            
            .search-suggestion:hover {
                background: #f8f9fa;
            }
            
            .theme-toggle {
                display: flex;
                align-items: center;
                gap: 0.5rem;
                margin-bottom: 1rem;
            }
            
            .load-more-btn {
                background: linear-gradient(135deg, #28a745 0%, #20c997 100%);
                color: white;
                padding: 0.75rem 2rem;
                border-radius: 25px;
                border: none;
                font-weight: 500;
                cursor: pointer;
                margin: 2rem auto;
                display: block;
                transition: all 0.3s ease;
            }
            
            .load-more-btn:hover {
                transform: translateY(-1px);
                box-shadow: 0 4px 12px rgba(40, 167, 69, 0.4);
            }
            
            @media (max-width: 768px) {
                .main-header h1 {
                    font-size: 2rem;
                }
                
                .article-meta {
                    flex-direction: column;
                    gap: 0.5rem;
                }
                
                .pagination-container {
                    flex-direction: column;
                    text-align: center;
                }
                
                .stat-number {
                    font-size: 1.5rem;
                }
                
                .article-card {
                    padding: 1rem;
                }
            }
        </style>
        """

# ─────────────────────────────────────────────────────────────────────────────
# 🛠️ Configuration
st.set_page_config(
    page_title="NewsPulseAI", 
    page_icon="📰",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Session state başlatma
if 'current_page' not in st.session_state:
    st.session_state.current_page = 1
if 'articles_per_page' not in st.session_state:
    st.session_state.articles_per_page = 10
if 'loaded_articles' not in st.session_state:
    st.session_state.loaded_articles = 10
if 'dark_mode' not in st.session_state:
    st.session_state.dark_mode = False
if 'search_history' not in st.session_state:
    st.session_state.search_history = []

# Tema CSS'ini uygula
st.markdown(get_theme_css(st.session_state.dark_mode), unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────────────────────
# 🎯 Header
st.markdown("""
<div class="main-header">
    <h1>📰 NewsPulseAI</h1>
    <p>AI-Powered News Analytics & Summarization Platform</p>
</div>
""", unsafe_allow_html=True)

# About section
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

# Tema geçişi
col1, col2 = st.sidebar.columns([1, 2])
with col1:
    if st.button("🌙" if not st.session_state.dark_mode else "☀️"):
        st.session_state.dark_mode = not st.session_state.dark_mode
        st.rerun()
with col2:
    st.write("Dark Mode" if st.session_state.dark_mode else "Light Mode")

# Sayfalama ayarları
st.sidebar.subheader("📄 Pagination")
pagination_mode = st.sidebar.radio(
    "Display Mode",
    ["Pagination", "Load More", "Show All"]
)

if pagination_mode == "Pagination":
    st.session_state.articles_per_page = st.sidebar.slider("Articles per page", 5, 50, 10)
elif pagination_mode == "Load More":
    st.session_state.loaded_articles = st.sidebar.slider("Initial articles", 5, 30, 10)

# Arama önerileri için geçmiş
def get_search_suggestions(query, history):
    if not query:
        return []
    suggestions = [h for h in history if query.lower() in h.lower() and h != query]
    return suggestions[:5]

# Arama kutusu
keyword = st.sidebar.text_input("🔎 Search Keywords", placeholder="Enter keywords...")

# Arama önerileri
if keyword and st.session_state.search_history:
    suggestions = get_search_suggestions(keyword, st.session_state.search_history)
    if suggestions:
        st.sidebar.write("💡 Suggestions:")
        for suggestion in suggestions:
            if st.sidebar.button(f"🔍 {suggestion}", key=f"suggest_{suggestion}"):
                keyword = suggestion
                st.rerun()

# Diğer filtreler
sentiment = st.sidebar.selectbox("😊 Sentiment Filter", ["All", "positive", "neutral", "negative"])
category = st.sidebar.selectbox("📂 Category Filter", ["All", "technology", "science", "business"])

# Arama geçmişine ekle
if keyword and keyword not in st.session_state.search_history:
    st.session_state.search_history.append(keyword)
    if len(st.session_state.search_history) > 10:
        st.session_state.search_history.pop(0)

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
fetch_count = 1000 if pagination_mode == "Show All" else 100

with st.spinner("Loading news articles..."):
    if category != "All":
        news = call_api("/category", {"category": category, "top": fetch_count})
    elif keyword:
        news = call_api("/search", {"q": keyword, "top": fetch_count})
    elif sentiment != "All":
        news = call_api("/sentiment", {"type": sentiment, "top": fetch_count})
    else:
        news = call_api("/news", {"top": fetch_count})

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
# 📰 Articles with Pagination
if news:
    st.markdown("## 📰 Latest Articles")
    
    # Sayfalama mantığı
    if pagination_mode == "Pagination":
        total_pages = math.ceil(len(news) / st.session_state.articles_per_page)
        start_idx = (st.session_state.current_page - 1) * st.session_state.articles_per_page
        end_idx = start_idx + st.session_state.articles_per_page
        displayed_articles = news[start_idx:end_idx]
        
        # Sayfalama kontrolleri
        st.markdown(f"""
        <div class="pagination-container">
            <div class="pagination-info">
                Showing {start_idx + 1}-{min(end_idx, len(news))} of {len(news)} articles (Page {st.session_state.current_page}/{total_pages})
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns([1, 2, 1])
        with col1:
            if st.button("⬅️ Previous", disabled=st.session_state.current_page <= 1):
                st.session_state.current_page -= 1
                st.rerun()
        
        with col2:
            # Sayfa numaraları
            page_cols = st.columns(min(5, total_pages))
            for i, page_col in enumerate(page_cols):
                page_num = i + max(1, st.session_state.current_page - 2)
                if page_num <= total_pages:
                    with page_col:
                        if st.button(str(page_num), key=f"page_{page_num}",
                                   disabled=page_num == st.session_state.current_page):
                            st.session_state.current_page = page_num
                            st.rerun()
        
        with col3:
            if st.button("Next ➡️", disabled=st.session_state.current_page >= total_pages):
                st.session_state.current_page += 1
                st.rerun()
    
    elif pagination_mode == "Load More":
        displayed_articles = news[:st.session_state.loaded_articles]
        
        if len(news) > st.session_state.loaded_articles:
            st.markdown(f"""
            <div class="pagination-container">
                <div class="pagination-info">
                    Showing {len(displayed_articles)} of {len(news)} articles
                </div>
            </div>
            """, unsafe_allow_html=True)
    
    else:  # Show All
        displayed_articles = news
    
    # Makaleleri göster
    for art in displayed_articles:
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
    
    # Load More butonu
    if pagination_mode == "Load More" and len(news) > st.session_state.loaded_articles:
        col1, col2, col3 = st.columns([1, 1, 1])
        with col2:
            if st.button("📄 Load More Articles", key="load_more"):
                st.session_state.loaded_articles += 10
                st.rerun()

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
            fig.update_layout(
                showlegend=True, 
                height=400, 
                font=dict(size=12),
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)'
            )
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
                height=400,
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)'
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