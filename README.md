# Job Vectorizer

A service that vectorizes job postings and CVs, stores embeddings in PostgreSQL (pgvector), and finds matches using cosine similarity.

## Features

- **Jobs consumer** — reads the `job` topic, builds an embedding from title, description, tags, and location, and saves the job to the database.
- **CV consumer** — reads the `cv_tasks` topic, extracts text from PDF/DOCX files, builds an embedding, updates the CV, and returns top job matches.
- Separate Kafka consumer per topic (base class `KafkaConsumerManager`).
- Embedding model: `sentence-transformers/all-MiniLM-L6-v2` (384 dimensions).

## Requirements

- Python >= 3.11
- PostgreSQL with the [pgvector](https://github.com/pgvector/pgvector) extension
- Apache Kafka (default: `localhost:9092`)

## Installation

```bash
git clone <repository-url>
cd job-vectorizer

python -m venv .venv
.venv\Scripts\activate   # Windows
# source .venv/bin/activate  # Linux/macOS

pip install -e .
# or: uv sync
```

Create a `.env` file in the project root with database settings (`DB_USERNAME`, `DB_PASSWORD`, `DB_DATABASE`, `DB_HOST`, `DB_PORT`). See your local deployment configuration for values.

## Running

From the `src` directory (or from the project root with `PYTHONPATH=src`):

```bash
cd src
python -m main
```

Stop with `Ctrl+C` — consumers shut down via `shutdown_consumers()`.

## Kafka

| Topic           | Consumer                 | Description                          |
|-----------------|--------------------------|--------------------------------------|
| `job`           | `jobs_consumer`          | New job postings (RemotiveJob JSON)  |
| `cv_tasks`      | `cv_consumer`            | CV processing tasks                  |
| `tasks`         | `tasks_consumer`         | Stub (enable in `main.py`)           |
| `notifications` | `notifications_consumer` | Stub                                 |

Example `cv_tasks` message:

```json
{
  "task_id": 1,
  "cv_id": 1,
  "file_path": "C:\\path\\to\\resume.pdf"
}
```

## Project structure

```
src/
├── main.py                 # Entry point, consumer threads
├── conf/                   # DB settings (.env)
├── consumers/
│   ├── kafka_consumer.py   # Base KafkaConsumerManager
│   ├── jobs_consumer.py
│   ├── cv_consumer.py
│   ├── tasks_consumer.py
│   └── notifications_consumer.py
├── services/
│   ├── embedding_service.py
│   └── job_ingest_service.py
├── repositories/           # Database access
├── models/                 # SQLAlchemy + Pydantic schemas
└── db/
    └── async_session_manager.py
```

## Dependencies

Main packages: `kafka-python`, `sentence-transformers`, `sqlalchemy`, `psycopg`, `pgvector`, `pydantic-settings`, `python-docx`, `pypdf`.

> For Kafka, use **`kafka-python`**, not the `kafka` package.

## Windows

On Windows, `WindowsSelectorEventLoopPolicy` is required for async psycopg (configured in `main.py` and `job_ingest_service.py`).

## Author

Anastasiia Odyntsova
