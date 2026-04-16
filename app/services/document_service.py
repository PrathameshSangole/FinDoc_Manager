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

def search_documents(db, title=None, company_name=None, document_type=None):
    query = db.query(Document)

    if title:
        query = query.filter(Document.title.contains(title))
    if company_name:
        query = query.filter(Document.company_name.contains(company_name))
    if document_type:
        query = query.filter(Document.document_type == document_type)

    return query.all()