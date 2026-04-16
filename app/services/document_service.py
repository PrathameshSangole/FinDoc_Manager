from sqlalchemy.orm import Session
from app.models.document import Document

def create_document(db: Session, data):
    doc = Document(**data.dict())
    db.add(doc)
    db.commit()
    db.refresh(doc)
    return doc

def get_all_documents(db: Session):
    return db.query(Document).all()

def get_document_by_id(db: Session, doc_id: int):
    return db.query(Document).filter(Document.id == doc_id).first()

def delete_document(db: Session, doc_id: int):
    doc = db.query(Document).filter(Document.id == doc_id).first()
    if doc:
        db.delete(doc)
        db.commit()
    return doc