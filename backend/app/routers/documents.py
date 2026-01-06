from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.schemas.document import DocumentsSchema
from app.models import Documents
from app.db import get_db

router = APIRouter()

# Documents
@router.get("/documents", response_model=list[DocumentsSchema])
async def get_documents(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Documents))
    return result.scalars().all()

@router.post("/documents", response_model=DocumentsSchema)
async def add_document(doc: DocumentsSchema, db: AsyncSession = Depends(get_db)):
    new_doc = Documents(**doc.dict(exclude_unset=True))
    db.add(new_doc)
    await db.commit()
    await db.refresh(new_doc)
    return new_doc