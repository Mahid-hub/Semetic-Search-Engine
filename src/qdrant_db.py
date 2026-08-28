import os
from dotenv import load_dotenv
from qdrant_client import QdrantClient
from qdrant_client.models import VectorParams, Distance, PointStruct
from ingest import load_documents
from chunker import chunk_text
from embeddings import embed_text

load_dotenv()

size = int(os.getenv('chunk-size'))
overlap = int(os.getenv('chunk-overlap'))
documents = load_documents('data/raw')
endPoint = os.getenv('Endpoint')
api_key = os.getenv('cluster-api-key')

client = QdrantClient(
    url=endPoint,
    api_key=api_key
)

if not client.collection_exists(collection_name=os.getenv('collection-name')):
    client.create_collection(
        collection_name=os.getenv('collection-name'),
        vectors_config=VectorParams(
            size=384,
            distance=Distance.COSINE
        )
    )
    
pointNo = 1

for doc in documents:    
    chunks = chunk_text(size, overlap, doc['text'], doc)
    
    for chunk in chunks:
        embedding = embed_text(chunk['text'])
   
        point = PointStruct(
            id=pointNo,
            vector= embedding.tolist(),
            payload={
                "chunk_id": chunk["chunk_id"],
                "document_id": chunk["document_id"],
                "source": chunk["source"],
                "text": chunk["text"]
            }
        )

        client.upsert(
            collection_name=os.getenv('collection-name'),
            points=[point]
        )
        pointNo += 1

print("Vector stored successfully!")
