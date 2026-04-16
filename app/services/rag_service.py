from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams, PointStruct
from sentence_transformers import SentenceTransformer
import re

client = QdrantClient(":memory:")
model = SentenceTransformer("all-MiniLM-L6-v2")

collection_name = "documents"

client.recreate_collection(
    collection_name=collection_name,
    vectors_config=VectorParams(size=384, distance=Distance.COSINE)
)

# ---------- Semantic Chunking ----------
def chunk_text(text: str):
    sentences = re.split(r'(?<=[.!?]) +', text)
    return [s.strip() for s in sentences if s.strip()]

# ---------- Index Document ----------
def index_document(doc_id: int, text: str):
    chunks = chunk_text(text)

    points = []
    for idx, chunk in enumerate(chunks):
        embedding = model.encode(chunk).tolist()

        points.append(
            PointStruct(
                id=doc_id * 100 + idx,
                vector=embedding,
                payload={
                    "text": chunk,
                    "doc_id": doc_id
                }
            )
        )

    client.upsert(
        collection_name=collection_name,
        points=points
    )

# ---------- Search + Reranking ----------
def search_documents(query: str):
    query_vector = model.encode(query)

    results = client.query_points(
        collection_name=collection_name,
        query=query_vector.tolist(),
        limit=20
    )

    reranked = []
    for point in results.points:
        chunk_text_data = point.payload["text"]
        chunk_vector = model.encode(chunk_text_data)

        score = float(query_vector @ chunk_vector)
        reranked.append((score, point))

    reranked.sort(key=lambda x: x[0], reverse=True)

    top_results = reranked[:5]

    return [{"text": p.payload["text"]} for _, p in top_results]

# ---------- Remove Document ----------
def remove_document(doc_id: int):
    results = client.scroll(
        collection_name=collection_name,
        scroll_filter=Filter(
            must=[
                FieldCondition(
                    key="doc_id",
                    match=MatchValue(value=doc_id)
                )
            ]
        )
    )

    ids_to_delete = [point.id for point in results[0]]

    if ids_to_delete:
        client.delete(
            collection_name=collection_name,
            points_selector=ids_to_delete
        )

# ---------- Get Context ----------
from qdrant_client.models import Filter, FieldCondition, MatchValue

def get_context(doc_id: int):
    results = client.scroll(
        collection_name=collection_name,
        scroll_filter=Filter(
            must=[
                FieldCondition(
                    key="doc_id",
                    match=MatchValue(value=doc_id)
                )
            ]
        )
    )

    return [point.payload["text"] for point in results[0]]