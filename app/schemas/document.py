from pydantic import BaseModel

class DocumentCreate(BaseModel):
    title: str
    company_name: str
    document_type: str
    uploaded_by: str