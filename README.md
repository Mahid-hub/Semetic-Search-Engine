# Semantic Search Engine

A semantic search engine built from scratch to compare **keyword search, dense vector search, and hybrid search** on a small technical-document corpus.

## What I Built

The system takes raw documents, splits them into chunks, generates embeddings for the chunks, stores them in **Qdrant**, and provides three search methods:

- BM25 Keyword Search
- Dense Semantic Search
- Hybrid Search using Reciprocal Rank Fusion (RRF)

## Project Pipeline

```text
Documents
    ↓
Document Ingestion
    ↓
Text Chunking + Chunk IDs
    ↓
Text Embeddings
    ↓
Qdrant Vector Database
    ↓
 ┌──────────────┬──────────────┐
 ↓              ↓              ↓
BM25         Dense Search   Hybrid Search
                               ↓
                              RRF
                               ↓
                         Ranked Results
                               ↓
                           Evaluation
```

## Corpus

The project uses a small technical corpus containing:

- Git
- Python
- JavaScript
- Linux

The documents are stored in:

```text
data/raw/
```

## Chunking

Documents are divided into smaller overlapping chunks.

Each chunk contains:

```text
chunk_id
document_id
source
text
```

Example:

```text
git_001
git_002
git_003
```

Chunking allows the search engine to retrieve the specific part of a document that is relevant to a query.

## Embeddings

Each text chunk is converted into a numerical vector using a **Hugging Face Sentence Transformer embedding model**.

The same embedding process is also applied to the user's search query.

```text
Text
 ↓
Embedding Model
 ↓
Vector
```

## Vector Database

The embeddings are stored in **Qdrant**.

Each vector is stored together with its metadata:

```text
Vector
+
Chunk ID
+
Document ID
+
Source
+
Text
```

Qdrant is used for vector similarity search and storing the metadata associated with each chunk.

## Dense Search

Dense search converts the user's query into an embedding and searches Qdrant for the most semantically similar chunks.

```text
User Query
    ↓
Embedding
    ↓
Query Vector
    ↓
Qdrant
    ↓
Top-K Similar Chunks
```

## Keyword Search

Keyword search uses **BM25**.

BM25 searches for matching words between the query and document chunks and assigns a relevance score to each chunk.

It works well when the query contains important exact keywords.

## Hybrid Search

Hybrid search combines BM25 and dense search.

```text
             Query
               ↓
       ┌───────┴───────┐
       ↓               ↓
     BM25            Dense
       ↓               ↓
       └───────┬───────┘
               ↓
              RRF
               ↓
        Final Ranking
```

The project uses **Reciprocal Rank Fusion (RRF)** to combine the rankings from both search methods.

## Evaluation

A small manually labeled query set is used as the ground truth.

Each query contains the chunk IDs that are considered relevant.

Example:

```json
{
    "query": "How do I create a Git branch?",
    "relevant_chunks": [
        "git_009",
        "git_010"
    ]
}
```

The following methods are compared:

```text
BM25
Dense Search
Hybrid Search
```

### Metrics

**Recall@5**

Measures how many relevant chunks were found in the top 5 results.

**MRR (Mean Reciprocal Rank)**

Measures how high the first relevant result appears in the ranking.

## Results

The final values are obtained by running:

```bash
python src/evaluate.py
```

## Project Structure

```text
Week_2/
│
├── data/
│   └── raw/
│       ├── git.txt
│       ├── python.txt
│       ├── javascript.txt
│       └── linux.txt
│
├── queries/
│   └── test_queries.json
│
├── src/
│   ├── ingest.py
│   ├── chunker.py
│   ├── embeddings.py
│   ├── dense_search.py
│   ├── keyword_search.py
│   ├── hybrid_search.py
│   └── evaluate.py
│
├── .env
├── .gitignore
├── requirements.txt
└── README.md
```

## How to Run

Create and activate the virtual environment:

```powershell
python -m venv venv
.env\Scripts\Activate.ps1
```

Install dependencies:

```powershell
pip install -r requirements.txt
```

Run dense search:

```powershell
python src/dense_search.py
```

Run keyword search:

```powershell
python src/keyword_search.py
```

Run hybrid search:

```powershell
python src/hybrid_search.py
```

Run evaluation:

```powershell
python src/evaluate.py
```

## What I Learned

- Document ingestion
- Text chunking
- Chunk IDs and metadata
- Text embeddings
- Vector databases
- Qdrant
- Dense semantic search
- BM25 keyword search
- Hybrid search
- Reciprocal Rank Fusion
- Retrieval evaluation
- Recall@5
- MRR

## Limitations

- The corpus is relatively small.
- The evaluation query set is small.
- Ground-truth labels are manually created.
- Search quality depends on chunk size and embedding model.
- The system currently focuses on retrieval and does not generate final answers using an LLM.

## Future Improvements

- Test multiple embedding models
- Experiment with different chunk sizes
- Add metadata filtering
- Increase the evaluation dataset
- Add a reranking model
- Build a complete RAG system with an LLM
