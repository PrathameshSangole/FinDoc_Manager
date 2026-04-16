from fastapi import APIRouter
from app.services.rag_service import (
    index_document,
    search_documents,
    remove_document,
    get_context
)

router = APIRouter()

@router.post("/index-document")
def index_doc(doc_id: int, text: str):
    index_document(doc_id, text)
    return {"message": "Document indexed"}

@router.post("/search")
def search(query: str):
    results = search_documents(query)
    return {"results": results}

@router.delete("/remove-document/{doc_id}")
def remove_doc(doc_id: int):
    remove_document(doc_id)
    return {"message": "Document embedding removed"}

@router.get("/context/{doc_id}")
def get_doc_context(doc_id: int):
    return {"context": get_context(doc_id)}