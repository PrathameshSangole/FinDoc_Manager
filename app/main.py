from fastapi import FastAPI
from app.database import Base, engine
from app.routes import auth, document, role, rag
from app.models import user, document as document_model, role as role_model

app = FastAPI(title="FinDoc Manager")

Base.metadata.create_all(bind=engine)

app.include_router(auth.router, prefix="/auth", tags=["Auth"])
app.include_router(document.router, prefix="/documents", tags=["Documents"])
app.include_router(role.router, prefix="/roles", tags=["Roles"])
app.include_router(rag.router, prefix="/rag", tags=["RAG"])

@app.get("/")
def root():
    return {"message": "FinDoc Manager API Running"}