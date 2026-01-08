from fastapi import APIRouter, Depends, UploadFile, File, Form, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.db import get_db
from app.models import Documents, JobSeeker, NlpLogs
from app.schemas.nlp_processing import ResumeParseResponse

import uuid


router = APIRouter(prefix="/nlp", tags=["NLP"])

#text extraction from format logic (ONLY TEXT AND PDF SUPPORTED)
def extract_text(file: UploadFile) -> str:
    if file.filename.endswith(".txt"):
        return file.file.read().decode("utf-8")

    if file.filename.endswith(".pdf"):
        raise HTTPException(
            status_code=415,
            detail="PDF parsing not implemented yet"
        )

    raise HTTPException(
        status_code=415,
        detail="Unsupported file type"
    )

#enpoint  for parsing 
@router.post("/resume/parse",response_model=ResumeParseResponse,status_code=status.HTTP_201_CREATED)
async def parse_resume(
    user_id: uuid.UUID = Form(...),
    file: UploadFile = File(...),
    db: AsyncSession = Depends(get_db)
):
    # Validate user
    user = await db.get(JobSeeker, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # Extract text
    extracted_text = extract_text(file)

    # Save document
    document = Documents(
        user_id=user_id,
        doc_type="resume",
        content=extracted_text,
        file_path=file.filename
    )
    db.add(document)

    # Log NLP run
    log = NlpLogs(
        model_name="resume_text_extraction_v1",
        notes=f"Parsed file: {file.filename}"
    )
    db.add(log)

    await db.commit()
    await db.refresh(document)

    return ResumeParseResponse(
        document_id=document.document_id,
        user_id=user_id,
        extracted_text=extracted_text,
        model_name=log.model_name
    )