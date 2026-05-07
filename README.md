# RAG Platform v4

A production-ready Retrieval-Augmented Generation (RAG) platform for domain-specific and general-purpose question answering. The system combines hybrid retrieval across multiple knowledge sources with large language models to deliver accurate, context-aware responses in areas such as healthcare, legal, psychology, and enterprise knowledge management.

Built with Python, PostgreSQL, ChromaDB, Celery, and Groq, the platform supports modular data ingestion, hybrid search (vector, keyword, and database retrieval), conversation persistence, and history-aware query rewriting for scalable knowledge retrieval.

Architecture
User Question
      │
      ▼
Hybrid Retriever
(Vector Search + Elasticsearch + Database Queries)
      │
      ▼
Context Aggregation
      │
      ▼
Prompt Template
      │
      ▼
Qwen3-32B (Groq)
      │
      ▼
Generated Answer

```
Embedding Model: sentence-transformers/all-MiniLM-L6-v2 (local inference via Hugging Face)

LLM: qwen/qwen3-32b served through Groq

A production-oriented Retrieval-Augmented Generation (RAG) platform built with Python, PostgreSQL, ChromaDB, Celery, and Groq LLMs.

The project is designed with modular ingestion, hybrid retrieval, conversation persistence, and history-aware query rewriting to provide accurate and scalable question answering over enterprise knowledge bases.
```
---

# Features

## Ingestion Pipeline

* PDF and document loading
* Automatic chunking
* Metadata extraction
* SHA-based file hash deduplication
* Original file storage
* PostgreSQL persistence
* ChromaDB vector indexing
* Asynchronous ingestion using Celery
* Ingestion job tracking

## Hybrid Retrieval

* Dense Vector Search (ChromaDB)
* BM25 Keyword Search
* Reciprocal Rank Fusion (RRF)
* Metadata Filtering
* Duplicate Chunk Removal
* Cross-Encoder Reranking

## Conversation Support

* Persistent Chat Sessions
* Persistent Chat Messages
* History-aware Query Rewriting

## Persistence

PostgreSQL stores:

* Documents
* Document Chunks
* Ingestion Jobs
* Chat Sessions
* Chat Messages

---

# Overall Architecture

```
                         ┌────────────────────────┐
                         │      User Query        │
                         └────────────┬───────────┘
                                      │
                                      ▼
                     ┌────────────────────────────────┐
                     │ History Aware Query Rewriter   │
                     └────────────────┬───────────────┘
                                      │
                                      ▼
                          Standalone Query Generated
                                      │
                                      ▼
                    ┌─────────────────────────────────┐
                    │      Hybrid Retrieval Layer      │
                    └──────────────┬───────────────────┘
                                   │
             ┌─────────────────────┴──────────────────────┐
             │                                            │
             ▼                                            ▼
   Dense Vector Retrieval                      BM25 Keyword Retrieval
      (ChromaDB)                                   (PostgreSQL)
             │                                            │
             └─────────────────────┬──────────────────────┘
                                   │
                                   ▼
                    Reciprocal Rank Fusion (RRF)
                                   │
                                   ▼
                        Metadata Filtering
                                   │
                                   ▼
                        Duplicate Removal
                                   │
                                   ▼
                      Cross Encoder Reranker
                                   │
                                   ▼
                            Final Context
                                   │
                                   ▼
                            Prompt Builder
                                   │
                                   ▼
                               Groq LLM
                                   │
                                   ▼
                           Final Answer
```

---

# Ingestion Workflow

```
PDF
 │
 ▼
Storage Service
 │
 ▼
Generate SHA File Hash
 │
 ├──────────── Duplicate?
 │             │
 │             ├── Yes → Return Existing Document
 │             │
 │             └── No
 ▼
Create Document Record
 │
 ▼
Create Ingestion Job
 │
 ▼
Celery Worker
 │
 ▼
Document Loader
 │
 ▼
Chunking
 │
 ▼
Metadata Extraction
 │
 ▼
Persist Chunk Metadata
 │
 ▼
Index into ChromaDB
 │
 ▼
Update Job Status
 │
 ▼
Document READY
```

---

# Retrieval Workflow

```
User Query
 │
 ▼
History-aware Rewrite
 │
 ▼
Dense Retrieval
 │
 ▼
BM25 Retrieval
 │
 ▼
Reciprocal Rank Fusion
 │
 ▼
Metadata Filter
 │
 ▼
Deduplicate
 │
 ▼
Cross Encoder Reranker
 │
 ▼
Prompt
 │
 ▼
Groq LLM
 │
 ▼
Answer
```

---

# Project Structure

```
rag_platform/
│
├── api/
├── common/
├── config/
├── database/
│   ├── entities/
│   ├── models/
│   └── repositories/
│
├── ingestion/
│   ├── chunking/
│   ├── hashing/
│   ├── indexing/
│   ├── loaders/
│   └── metadata/
│
├── retrieval/
│   ├── filters/
│   ├── fusion/
│   ├── keyword_search/
│   ├── query_rewrite/
│   ├── reranker/
│   └── vector_search/
│
├── services/
├── storage/
├── workers/
├── tests/
└── rag_chain.py (legacy / optional)
```

---

# Tech Stack

* Python 3.11+
* PostgreSQL
* SQLAlchemy
* ChromaDB
* LangChain
* Groq LLM
* Celery
* Redis
* rank-bm25

---

# Installation

## Clone repository

```bash
git clone https://github.com/akaspringfield/rag-pipeline-architecture.git
cd rag_platform
```

## Create virtual environment

```bash
python -m venv .venv
```

Windows:

```bash
.venv\Scripts\activate
```

Linux/macOS:

```bash
source .venv/bin/activate
```

## Install dependencies

```bash
pip install -r requirements.txt
```

---

# PostgreSQL

Create a database:

```sql
CREATE DATABASE rag_platform;
```

Configure `.env` or settings:

```
DATABASE_URL=postgresql://postgres:password@localhost:5432/rag_platform
```

---

# Database Migration

If using Alembic:

```bash
alembic revision --autogenerate -m "Initial migration"
alembic upgrade head
```

To generate future migrations:

```bash
alembic revision --autogenerate -m "Describe changes"
alembic upgrade head
```

---

# Redis

Start Redis before Celery.

Default:

```
localhost:6379
```

---

# Start Celery Worker

```bash
celery -A workers.celery_app worker --loglevel=info
```

---

# Run the API

Example:

```bash
python app.py
```
or

```bash
uvicorn api.main:app --reload
```
Opens at `http://localhost:8501`. The sidebar has one-click sample questions and a button to clear the conversation history.

```
Interactive prompt — type a question and press Enter. Type `quit` to exit.
---

# Run Tests

Example:

```bash
python -m tests.unit.test_ingestion
python -m tests.unit.test_bm25_database
python -m tests.unit.test_history_rewriter
python -m tests.unit.test_chat_service
```

---

# Current Status

| Feature                       | Status  |
| ----------------------------- | ------- |
| File Storage                  | ✅       |
| Hash Deduplication            | ✅       |
| Chunking                      | ✅       |
| Metadata Extraction           | ✅       |
| PostgreSQL Persistence        | ✅       |
| Celery Ingestion              | ✅       |
| ChromaDB Indexing             | ✅       |
| Dense Retrieval               | ✅       |
| BM25 Retrieval                | ✅       |
| Reciprocal Rank Fusion        | ✅       |
| Metadata Filtering            | ✅       |
| Cross Encoder Reranking       | ✅       |
| Conversation Persistence      | ✅       |
| History-aware Query Rewriting | ✅       |
| Source Citations              | Planned |
| Multi-query Retrieval         | Planned |

---

# Production Roadmap

* Source citations in responses
* Multi-query retrieval
* Query expansion
* Evaluation benchmarks
* Retrieval metrics dashboard
* Streaming responses
* Multi-tenant authorization
* Automatic BM25 refresh
* Distributed ingestion workers

---

# Automated Setup Script

Save the following as `setup_project.py`:

```python
import os
import subprocess
import sys

def run(command):
    print(f"Running: {command}")
    subprocess.check_call(command, shell=True)

run(f"{sys.executable} -m venv .venv")

if os.name == "nt":
    pip = r".venv\Scripts\pip"
else:
    pip = "./.venv/bin/pip"

run(f"{pip} install -r requirements.txt")

print()
print("Installation complete.")
print()
print("Next steps:")
print("1. Start PostgreSQL")
print("2. Start Redis")
print("3. Run Alembic migrations")
print("4. Start Celery:")
print("   celery -A workers.celery_app worker --loglevel=info")
print("5. Start your API application")
```
---

## Data Sources
We have created default embeddings with different domains. The retriever fetches the top N results from each collection (N context documents total) for every query.