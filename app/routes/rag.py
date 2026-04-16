from fastapi import APIRouter
from app.services.rag_service import index_document, search_documents

router = APIRouter()

@router.post("/index-document")
def index_doc(doc_id: int, text: str):
    index_document(doc_id, text)
    return {"message": "Document indexed"}

@router.post("/search")
def search(query: str):
    results = search_documents(query)
    return {"results": results}