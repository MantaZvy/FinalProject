from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.schemas.document import DocumentCreate, DocumentUpdate, DocumentOut
from app.models import Documents, JobSeeker
from app.db import get_db

router = APIRouter(prefix="/documents", tags=["Documents"])

# Documents
#Create
@router.post("/", response_model=DocumentOut, status_code=status.HTTP_201_CREATED)
async def create_document(payload: DocumentCreate, db: AsyncSession = Depends(get_db)):
    # Ensure user exists
    user = await db.scalar(select(JobSeeker).where(JobSeeker.user_id == payload.user_id))
    if not user:
        raise HTTPException(status_code=400, detail="Invalid user_id")

    doc = Documents(**payload.model_dump())
    db.add(doc)
    await db.commit()
    await db.refresh(doc)
    return doc
#Get by ID
@router.get("/{document_id}", response_model=DocumentOut)
async def get_document(document_id: str, db: AsyncSession = Depends(get_db)):
    doc = await db.scalar(select(Documents).where(Documents.document_id == document_id))
    if not doc:
        raise HTTPException(status_code=404, detail="Document not found")
    return doc

#Get All
@router.get("/", response_model=list[DocumentOut])
async def get_documents(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Documents))
    return result.scalars().all()

#Update
@router.put("/{document_id}", response_model=DocumentOut)
async def update_document(document_id: str, payload: DocumentUpdate, db: AsyncSession = Depends(get_db)):
    doc = await db.scalar(select(Documents).where(Documents.document_id == document_id))
    if not doc:
        raise HTTPException(status_code=404, detail="Document not found")

    for field, value in payload.model_dump(exclude_unset=True).items():
        setattr(doc, field, value)

    await db.commit()
    await db.refresh(doc)
    return doc

#Delete
@router.delete("/{document_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_document(document_id: str, db: AsyncSession = Depends(get_db)):
    doc = await db.scalar(select(Documents).where(Documents.document_id == document_id))
    if not doc:
        raise HTTPException(status_code=404, detail="Document not found")

    await db.delete(doc)
    await db.commit()