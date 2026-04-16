from pydantic import BaseModel, field_validator

class DocumentCreate(BaseModel):
    title: str
    company_name: str
    document_type: str
    uploaded_by: str

    @field_validator("document_type")
    def validate_type(cls, v):
        allowed = ["invoice", "report", "contract"]
        if v.lower() not in allowed:
            raise ValueError("document_type must be invoice, report, or contract")
        return v.lower()