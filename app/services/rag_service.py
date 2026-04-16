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
    chunks = [text[i:i+200] for i in range(0, len(text), 200)]

    points = []
    for idx, chunk in enumerate(chunks):
        embedding = model.encode(chunk).tolist()
        points.append(
            PointStruct(
                id=doc_id * 100 + idx,
                vector=embedding,
                payload={"text": chunk, "doc_id": doc_id}
            )
        )

    client.upsert(
        collection_name=collection_name,
        points=points
    )

def search_documents(query: str):
    query_vector = model.encode(query).tolist()

    results = client.query_points(
        collection_name=collection_name,
        query=query_vector,
        limit=20
    )

    sorted_results = sorted(results.points, key=lambda x: x.score, reverse=True)

    top_results = sorted_results[:5]

    return [{"text": point.payload["text"]} for point in top_results]

def remove_document(doc_id: int):
    client.delete(
        collection_name=collection_name,
        points_selector=[doc_id]
    )

def get_context(doc_id: int):
    results = client.scroll(
        collection_name=collection_name,
        scroll_filter={
            "must": [
                {
                    "key": "doc_id",
                    "match": {"value": doc_id}
                }
            ]
        }
    )

    return [point.payload["text"] for point in results[0]]