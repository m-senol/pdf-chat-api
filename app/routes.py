from fastapi import APIRouter, HTTPException, UploadFile, File
from uuid import uuid4
from fastapi.responses import JSONResponse
from .services import validate_file
from .db_operations import insert_pdf_data, get_pdf_by_id
from .services import extract_info_from_pdf, get_ai_response
from .config import (
    PDF_NOT_FOUND_ERROR_CODE, PDF_NOT_FOUND_ERROR_TEXT,
    NO_MESSAGE_ERROR_CODE, NO_MESSAGE_ERROR_TEXT
)
from .logger import logger

router = APIRouter()

@router.post("/v1/pdf")
async def upload_pdf(file: UploadFile = File(...)):
    logger.info(f"Received file upload request")
    contents = await validate_file(file)
    pdf_id = str(uuid4())
    extracted_text, page_count = await extract_info_from_pdf(contents)
    await insert_pdf_data(pdf_id, file.filename, page_count, extracted_text)
    logger.info(f"PDF data inserted into database")
    return JSONResponse(content={"pdf_id": pdf_id})

@router.post("/v1/chat/{pdf_id}")
async def chat_with_pdf(pdf_id: str, request_body: dict):
    logger.info(f"Recieved chat request")
    user_message = request_body.get("message")
    if not user_message:
        logger.error(f"No message provided")
        raise HTTPException(status_code=NO_MESSAGE_ERROR_CODE, detail=NO_MESSAGE_ERROR_TEXT)
    
    pdf_data = await get_pdf_by_id(pdf_id)
    if not pdf_data:
        logger.error(f"PDF ID not in database")
        raise HTTPException(status_code=PDF_NOT_FOUND_ERROR_CODE, detail=PDF_NOT_FOUND_ERROR_TEXT)
    
    pdf_content = pdf_data["content"]
    ai_response = await get_ai_response(pdf_content, user_message)

    logger.info(f"AI response is generated")
    return {"response": ai_response}
