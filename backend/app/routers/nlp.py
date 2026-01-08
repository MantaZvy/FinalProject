from fastapi import APIRouter, Depends, UploadFile, File, Form, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.db import get_db
from app.models import Documents, JobSeeker, NlpLogs
from app.schemas.nlp_processing import ResumeParseResponse
from app.nlp.resume_parser import extract_resume_text, parse_resume

import uuid

router = APIRouter(prefix="/nlp", tags=["NLP"])

@router.post(
    "/resume/parse",
    response_model=ResumeParseResponse,
    status_code=status.HTTP_201_CREATED
)
async def parse_resume_endpoint(
    user_id: uuid.UUID = Form(...),
    file: UploadFile = File(...),
    db: AsyncSession = Depends(get_db)
):
    #validate user
    user = await db.get(JobSeeker, user_id)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    #read file contents asynchronously
    file_bytes = await file.read()
    if not file_bytes:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Uploaded file is empty"
        )

    #extract raw text from uploaded file
    extracted_text = extract_resume_text(file_bytes=file_bytes, content_type=file.content_type)

    #parse structured resume data
    parsed = parse_resume(extracted_text)

    #persist raw document
    document = Documents(
        user_id=user_id,
        doc_type="resume",
        content=extracted_text,
        file_path=file.filename
    )
    db.add(document)

    #update JobSeeker with parsed fields
    if parsed.get("skills"):
        user.skills = parsed["skills"]
    if parsed.get("keywords"):
        user.keywords = parsed["keywords"]
    if parsed.get("profile_summary"):
        user.profile_summary = parsed["profile_summary"]
    if parsed.get("education"):
        user.education = {"education": parsed["education"]}
    if parsed.get("experience"):
        user.experience = {"experience": parsed["experience"]}

    #log NLP execution
    log = NlpLogs(
        model_name="resume_text_extraction_v1",
        notes=f"Parsed file: {file.filename}"
    )
    db.add(log)

    #commit transaction
    await db.commit()
    await db.refresh(document)
    await db.refresh(log)

    #return structured response
    return ResumeParseResponse(
        document_id=document.document_id,
        user_id=user_id,
        extracted_text=extracted_text,
        model_name=log.model_name,
        parsed_resume=parsed
    )