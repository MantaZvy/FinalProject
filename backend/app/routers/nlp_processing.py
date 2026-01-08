from fastapi import APIRouter, Depends, UploadFile, File, Form, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.db import get_db
from app.models import Documents, JobSeeker, NlpLogs
from app.schemas.nlp_processing import ResumeParseResponse

import uuid
import pdfplumber
from io import BytesIO



router = APIRouter(prefix="/nlp", tags=["NLP"])

#text extraction from format logic (ONLY TEXT AND PDF SUPPORTED)
def extract_text(file_bytes: bytes, content_type: str) -> str:

    if content_type == "text/plain":
        return file_bytes.decode("utf-8")

    if content_type == "application/pdf":
        text_chunks = []
        with pdfplumber.open(BytesIO(file_bytes)) as pdf:
            for page in pdf.pages:
                text_chunks.append(page.extract_text() or "")
        return "\n".join(text_chunks)
    
    raise HTTPException(
        status_code=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
        detail="Unsupported file type"
    )


#enpoint  for parsing 
@router.post(
    "/resume/parse",
    response_model=ResumeParseResponse,
    status_code=status.HTTP_201_CREATED
)
async def parse_resume(
    user_id: uuid.UUID = Form(...),
    file: UploadFile = File(...),
    db: AsyncSession = Depends(get_db)
):
    # Validate user
    user = await db.get(JobSeeker, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # Read file contents (async-safe)
    file_bytes = await file.read()

    if not file_bytes:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Uploaded file is empty"
        )

    # Extract text
    extracted_text = extract_text(
        file_bytes=file_bytes,
        content_type=file.content_type
    )

    # Persist document
    document = Documents(
        user_id=user_id,
        doc_type="resume",
        content=extracted_text,
        file_path=file.filename
    )
    db.add(document)

    # Log NLP execution
    log = NlpLogs(
        model_name="resume_text_extraction_v1",
        notes=f"Parsed file: {file.filename}"
    )
    db.add(log)

    await db.commit()
    await db.refresh(document)
    await db.refresh(log)

    return ResumeParseResponse(
        document_id=document.document_id,
        user_id=user_id,
        extracted_text=extracted_text,
        model_name=log.model_name
    )
