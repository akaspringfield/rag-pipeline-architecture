# RAG Telecom Chatbot

A Retrieval-Augmented Generation (RAG) general purpose chatbot for multiple senario it support. It answers questions about physology, legal, and medical by retrieving relevant context from different knowledge sources and generating responses with Qwen3-32B via Groq.

## Architecture

```
User question
     │
     ▼
Merged Retriever (top-k from each store)
  knowledge base (vector, elastic/hybrid,DB queries)
     │
     ▼
ChatPromptTemplate → Qwen3-32B (Groq) → Answer
```

**Embedding model:** `sentence-transformers/all-MiniLM-L6-v2` (runs locally via HuggingFace)  
**LLM:** `qwen/qwen3-32b` served by [Groq](https://groq.com)

## Project Structure

```
├rag_platform/

├── api/
│   ├── rest_api/
│   │   ├── routes.py
│   │   ├── schemas.py
│   │   └── dependencies.py
│   │
│   ├── grpc_api/
│   │   ├── service.py
│   │   └── proto/
│   │
│   └── main.py
│
├── workflow_router/
│   ├── router.py
│   └── registry.py
│
├── workflows/
│   ├── base_workflow.py
│   │
│   ├── physiology/
│   │   ├── workflow.py
│   │   ├── prompts.py
│   │   └── schemas.py
│   │
│   ├── recommendation/
│   │   ├── workflow.py
│   │   ├── scorer.py
│   │   └── schemas.py
│   │
│   ├── knowledge/
│   │   ├── workflow.py
│   │   └── schemas.py
│   │
│   └── report/
│       ├── workflow.py
│       └── schemas.py
│
├── query_processing/
│   ├── classifier/
│   │   └── service.py
│   │
│   ├── rewriter/
│   │   └── service.py
│   │
│   ├── decomposition/
│   │   └── service.py
│   │
│   └── memory/
│       └── service.py
│
├── retrieval/
│   ├── vector_search/
│   │   └── service.py
│   │
│   ├── hybrid_search/
│   │   └── service.py
│   │
│   ├── reranker/
│   │   └── service.py
│   │
│   └── compression/
│       └── service.py
│
├── reasoning/
│   ├── symptom_analysis/
│   │   └── service.py
│   │
│   ├── root_cause/
│   │   └── service.py
│   │
│   ├── evidence_builder/
│   │   └── service.py
│   │
│   └── confidence/
│       └── service.py
│
├── recommendation/
│   ├── retrieval/
│   │   └── service.py
│   │
│   ├── ranking/
│   │   └── service.py
│   │
│   ├── scoring/
│   │   └── service.py
│   │
│   └── explanation/
│       └── service.py
│
├── generation/
│   ├── prompts/
│   │   ├── physiology.py
│   │   ├── recommendation.py
│   │   └── knowledge.py
│   │
│   ├── response_builder.py
│   └── service.py
│
├── models/
│   ├── registry/
│   │   └── registry.py
│   │
│   ├── router/
│   │   └── router.py
│   │
│   └── providers/
│       ├── openai.py
│       ├── groq.py
│       └── ollama.py
│
├── ingestion/
│   ├── loaders/
│   │   ├── pdf_loader.py
│   │   ├── csv_loader.py
│   │   └── web_loader.py
│   │
│   ├── chunking/
│   │   └── service.py
│   │
│   ├── embeddings/
│   │   └── service.py
│   │
│   └── indexing/
│       └── service.py
│
├── evaluation/
│   ├── ragas/
│   ├── deepeval/
│   └── custom_metrics/
│
├── observability/
│   ├── logging/
│   │   └── logger.py
│   │
│   ├── metrics/
│   │   └── metrics.py
│   │
│   └── tracing/
│       └── tracing.py
│
├── databases/
│   ├── postgres/
│   │   └── connection.py
│   │
│   ├── vector_db/
│   │   └── qdrant.py
│   │
│   └── redis/
│       └── cache.py
│
├── workers/
│   ├── ingestion_worker.py
│   └── evaluation_worker.py
│
├── shared/
│   ├── config.py
│   ├── constants.py
│   ├── exceptions.py
│   └── utils.py
│
├── tests/
│   ├── unit/
│   ├── integration/
│   └── e2e/
│
├── requirements.txt
├── docker-compose.yml
└── README.md
├── pyproject.toml
├── uv.lock
├── .env
└── .env.example
```

## Prerequisites

- Python 3.10+
- [uv](https://docs.astral.sh/uv/) (recommended) or pip
- A [HuggingFace token](https://huggingface.co/settings/tokens) (for downloading the embedding model)
- A [Groq API key](https://console.groq.com)

## Setup

**1. Clone and install dependencies**

```bash
git clone <repo-url>
cd rag_platform
uv sync          # or: pip install -e .
```

**2. Configure environment variables**

```bash
cp .env.example .env
```

Edit `.env` and fill in your keys:

```
GROQ_API_KEY=your_groq_api_key_here
HF_TOKEN=your_huggingface_token_here
```

**3. Ingest data into Chroma**

Run the scripts as mentioned in project-readme:

```bash

```

Each script embeds the source data and persists it to `chroma_store/`. Re-run a script only when its source data changes.

## Running the App

**Uvicorn**

```bash
uvicorn api.main:app --reload  
```

Opens at `http://localhost:8501`. The sidebar has one-click sample questions and a button to clear the conversation history.

**CLI**

```bash
python main.py
```

Interactive prompt — type a question and press Enter. Type `quit` to exit.

## Data Sources
We have created default embeddings with different domains. The retriever fetches the top N results from each collection (N context documents total) for every query.
