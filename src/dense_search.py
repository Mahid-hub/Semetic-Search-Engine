import os
from dotenv import load_dotenv
from src.embeddings import embed_text
from qdrant_client import QdrantClient

load_dotenv()

endPoint = os.getenv('Endpoint')
api_key = os.getenv('cluster-api-key')

client = QdrantClient(
    url=endPoint,
    api_key=api_key,
    timeout=60
)

def dense_search(user_query, limit=5):
    
    embed_query = embed_text(user_query)
    result = client.query_points(
        collection_name=os.getenv('collection-name'),
        query=embed_query,
        limit=limit,
        with_payload=True,
        timeout=60
    )
    
    results = []
    for point in result.points:
        result_item = {
            "chunk_id": point.payload["chunk_id"],
            "document_id": point.payload["document_id"],
            "source": point.payload["source"],
            "text": point.payload["text"],
            "score": point.score
        }

        results.append(result_item)

    return results
