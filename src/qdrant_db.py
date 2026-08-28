import os
from dotenv import load_dotenv

from qdrant_client import QdrantClient
from qdrant_client.models import VectorParams, Distance, PointStruct

from src.ingest import load_documents
from src.chunker import chunk_text
from src.embeddings import embed_text

load_dotenv()


def get_client():
    endpoint = os.getenv("Endpoint")
    api_key = os.getenv("cluster-api-key")

    return QdrantClient(
        url=endpoint,
        api_key=api_key,
        timeout=60
    )


def index_documents():
    client = get_client()
    collection_name = os.getenv("collection-name")
    chunk_size = int(os.getenv("chunk-size"))
    chunk_overlap = int(os.getenv("chunk-overlap"))
    documents = load_documents("data/raw")

    if not client.collection_exists(collection_name=collection_name):
        client.create_collection(
            collection_name=collection_name,
            vectors_config=VectorParams(
                size=384,
                distance=Distance.COSINE
            )
        )
        print(f"Collection '{collection_name}' created.")
    else:
        print(f"Collection '{collection_name}' already exists.")

    point_number = 1
    for doc in documents:
        chunks = chunk_text(chunk_size, chunk_overlap, doc["text"], doc)
        print(f"\nIndexing: {doc['source']}")
        print(f"Chunks: {len(chunks)}")

        for chunk in chunks:
            embedding = embed_text(chunk["text"])
            point = PointStruct(
                id=point_number,
                vector=embedding.tolist(),
                payload={
                    "chunk_id": chunk["chunk_id"],
                    "document_id": chunk["document_id"],
                    "source": chunk["source"],
                    "text": chunk["text"]
                }
            )
            client.upsert(
                collection_name=collection_name,
                points=[point]
            )
            point_number += 1

    print("\n" + "=" * 60)
    print("DOCUMENT INDEXING COMPLETED")
    print("=" * 60)
    print(f"Documents indexed: {len(documents)}")
    print(f"Total points: {point_number - 1}")
