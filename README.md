# 🌐 NewsPulseAI (Lite)

> Demo-grade News Analytics & Summarization Platform powered by Azure AI Services

[![Azure AI](https://img.shields.io/badge/Azure%20AI-Powered-0078D4?style=for-the-badge&logo=microsoft-azure&logoColor=white)](https://azure.microsoft.com/services/cognitive-services/)
[![Python 3.10](https://img.shields.io/badge/Python-3.10-blue?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.95.0-009688?style=for-the-badge&logo=fastapi)](https://fastapi.tiangolo.com)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.31.0-FF4B4B?style=for-the-badge&logo=streamlit)](https://streamlit.io)
[![License](https://img.shields.io/badge/License-MIT-green.svg?style=for-the-badge)](LICENSE)

## 📋 Overview

NewsPulseAI is a lightweight news analytics platform that leverages Azure's AI capabilities to deliver real-time insights. This demo implementation showcases core functionalities using minimal cloud resources and simplified architecture.

### 🎯 Core Capabilities

#### Data Ingestion & Processing
- **NewsAPI Integration**
  - 100 requests/day free tier
  - Simple REST API access
- **Automated Processing Pipeline**
  - GitHub Actions scheduled triggers
  - Basic data validation
  - Blob storage persistence

#### AI-Powered Analysis
- **Natural Language Processing**
  - Abstractive Summarization using Azure AI Language
  - Sentiment Analysis
  - Key Phrase Extraction
- **Search Capabilities**
  - Vector similarity search
  - Basic trend detection

#### Interactive Features
- **RAG-enhanced Q&A System**
  - Azure OpenAI integration
  - Context-aware responses
- **Real-time Dashboard**
  - Sentiment visualization
  - Topic clouds

## 🏗️ Technical Architecture

```mermaid
flowchart LR
    subgraph Data Ingestion
        A1[NewsAPI] --> P[ingest_news.py]
        P -->|Scheduled Trigger| GH[GitHub Actions]
        GH -->|JSON| B[Blob Storage]
    end
    
    subgraph Storage & Processing
        B -->|Indexer| C[Azure AI Search]
        C -->|Vector Index| D[Search API]
    end

    subgraph Analysis & Presentation
        D -->|Query| R[RAG Engine]
        R -->|NLP| L[Azure Language]
        R -->|LLM| O[Azure OpenAI]
        R -->|API| F[FastAPI Backend]
        F -->|UI| S[Streamlit Dashboard]
    end
```

## 🛠️ Technical Stack Details

### Backend Infrastructure
- **Core Runtime**: Python 3.10
  - Basic async support
  - Type hints
- **API Layer**: FastAPI 0.95.0
  - REST endpoints
  - OpenAPI documentation
- **Data Storage**
  - Azure Blob Storage
  - JSON format

### Azure Services Configuration
- **Azure AI Services**
  - Language API (S0 tier)
  - OpenAI Service
- **Azure Blob Storage**
  - Basic tier
  - Single container
- **Azure AI Search**
  - Vector search
  - Basic tier

### Frontend Implementation
- **Streamlit Dashboard**
  - Simple components
  - Real-time updates
- **Basic Visualization**
  - Streamlit native charts
  - Word clouds

## 🚀 Development Setup

### Environment Configuration

```bash
# Create Python virtual environment
python -m venv .venv

# Activate virtual environment
source .venv/bin/activate  # Linux/macOS
.venv\Scripts\activate     # Windows

# Install dependencies
pip install -r requirements.txt
```

### Required Environment Variables

```bash
# Azure AI Services Configuration
AZURE_AI_ENDPOINT="https://<region>.api.cognitive.microsoft.com/"
AZURE_AI_KEY="your-key-here"

# Azure Storage Configuration
STORAGE_CONN_STR="DefaultEndpointsProtocol=https;AccountName=..."
BLOB_CONTAINER="news"

# Azure AI Search Configuration
SEARCH_ENDPOINT="https://<name>.search.windows.net"
SEARCH_KEY="your-search-key"
SEARCH_INDEX_NAME="news-index"

# News API Configuration
NEWSAPI_KEY="your-newsapi-key"
```

### Local Development

```bash
# Start development server
uvicorn backend.main:app --reload --port 8000

# Launch dashboard
streamlit run dashboard/app.py
```

## 📈 Performance & Costs

### Processing Metrics
- Batch Processing: ~30 articles/batch
- Processing Time: ~2s/article

### Cost Analysis (Estimated Monthly)
- Language API: ~$0.1/10K characters
- Blob Storage: <$0.1/GB
- AI Search: ~$0.5/1000 queries
- Total: Under $10/month for demo usage

## 🔒 Security

- Basic authentication
- Environment variables
- Azure Key management

## 📚 API Documentation

Available at `http://localhost:8000/docs`

## 🔄 CI/CD

```yaml
name: NewsPulseAI
on:
  schedule:
    - cron: '*/30 * * * *'
  workflow_dispatch:

jobs:
  ingest:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: '3.10'
      - run: pip install -r requirements.txt
      - run: python ingest_news.py
```

## 📄 License

MIT License - see [LICENSE](LICENSE) file

---
Built with Azure AI Services 🚀