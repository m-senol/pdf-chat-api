from app.db import database
from app.models import pdf_texts
from datetime import datetime, timezone
from fastapi import HTTPException
from .config import PDF_NOT_FOUND_ERROR_CODE, PDF_NOT_FOUND_ERROR_TEXT

async def insert_pdf_data(pdf_id: str, filename: str, page_count: int, extracted_text: str):
    query = pdf_texts.insert().values(
        id=pdf_id,
        filename=filename,
        page_count=page_count,
        content=extracted_text,
        upload_date=datetime.now(timezone.utc).isoformat()
    )
    await database.execute(query)

async def get_pdf_by_id(pdf_id: str):
    query = pdf_texts.select().where(pdf_texts.c.id == pdf_id)
    return await database.fetch_one(query)