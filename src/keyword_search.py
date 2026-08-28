import os
from dotenv import load_dotenv
from src.ingest import load_documents
from src.chunker import chunk_text
from rank_bm25 import BM25Okapi

load_dotenv()

size = int(os.getenv("chunk-size"))
overlap = int(os.getenv("chunk-overlap"))
documents = load_documents("data/raw")

all_chunks = []
for doc in documents:
    chunks = chunk_text(size, overlap, doc["text"], doc)
    all_chunks.extend(chunks)

tokenized_chunks = []
for chunk in all_chunks:
    text = chunk["text"]
    tokenized_chunks.append(text.lower().split())
    
bm25 = BM25Okapi(tokenized_chunks)

def keyword_search(query, limit):

    query_tokens = query.lower().split()
    scores = bm25.get_scores(query_tokens)

    ranked_indexes = sorted(
        range(len(scores)),
        key=lambda i:scores[i],
        reverse=True
    )

    results = []
    for index in ranked_indexes[:limit]:
        result = {
            "chunk_id": all_chunks[index]["chunk_id"],
            "document_id": all_chunks[index]["document_id"],
            "source": all_chunks[index]["source"],
            "text": all_chunks[index]["text"],
            "score": float(scores[index])
        }

        results.append(result)

    return results

