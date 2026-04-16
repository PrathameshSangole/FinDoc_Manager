from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.schemas.document import DocumentCreate
from app.services.document_service import (
    create_document,
    get_all_documents,
    get_document_by_id,
    delete_document
)

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/upload")
def upload_document(doc: DocumentCreate, db: Session = Depends(get_db)):
    new_doc = create_document(db, doc)
    return new_doc

@router.get("/")
def get_documents(db: Session = Depends(get_db)):
    return get_all_documents(db)

@router.get("/{doc_id}")
def get_document(doc_id: int, db: Session = Depends(get_db)):
    doc = get_document_by_id(db, doc_id)
    if not doc:
        raise HTTPException(status_code=404, detail="Document not found")
    return doc

@router.delete("/{doc_id}")
def delete_doc(doc_id: int, db: Session = Depends(get_db)):
    doc = delete_document(db, doc_id)
    if not doc:
        raise HTTPException(status_code=404, detail="Document not found")
    return {"message": "Document deleted"}