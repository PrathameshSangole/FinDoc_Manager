from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams
from sentence_transformers import SentenceTransformer

client = QdrantClient(":memory:")
model = SentenceTransformer("all-MiniLM-L6-v2")

collection_name = "documents"

client.recreate_collection(
    collection_name=collection_name,
    vectors_config=VectorParams(size=384, distance=Distance.COSINE)
)

from qdrant_client.models import PointStruct

def index_document(doc_id: int, text: str):
    embedding = model.encode(text).tolist()

    client.upsert(
        collection_name=collection_name,
        points=[
            PointStruct(
                id=doc_id,
                vector=embedding,
                payload={"text": text}
            )
        ]
    )

def search_documents(query: str):
    query_vector = model.encode(query).tolist()

    results = client.query_points(
        collection_name=collection_name,
        query=query_vector,
        limit=5
    )

    return [{"text": point.payload["text"]} for point in results.points]