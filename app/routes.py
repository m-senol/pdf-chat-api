from fastapi import APIRouter, HTTPException, UploadFile, File
from uuid import uuid4
from fastapi.responses import JSONResponse
from .services import validate_file
from .db_operations import insert_pdf_data, get_pdf_by_id
from .services import extract_info_from_pdf, get_ai_response

router = APIRouter()

@router.post("/v1/pdf")
async def upload_pdf(file: UploadFile = File(...)):
    contents = await validate_file(file)
    pdf_id = str(uuid4())
    extracted_text, page_count = await extract_info_from_pdf(contents)
    await insert_pdf_data(pdf_id, file.filename, page_count, extracted_text)
    return JSONResponse(content={"pdf_id": pdf_id})

@router.post("/v1/chat/{pdf_id}")
async def chat_with_pdf(pdf_id: str, request_body: dict):
    user_message = request_body.get("message")
    if not user_message:
        raise HTTPException(status_code=400, detail="Message is required")
    
    pdf_data = await get_pdf_by_id(pdf_id)
    if not pdf_data:
        raise HTTPException(status_code=404, detail="PDF not found")
    
    pdf_content = pdf_data["content"]
    ai_response = await get_ai_response(pdf_content, user_message)

    return {"response": ai_response}
