from fastapi import UploadFile
from pdf_processing.extract_pdf_info import extract_info
from asyncio import to_thread, wait_for, TimeoutError
from .config import (
    MAX_FILE_SIZE, TIMEOUT_TIME,
    FILE_NOT_VALID_PDF_ERROR_CODE, FILE_NOT_VALID_PDF_ERROR_TEXT, 
    FILE_TOO_BIG_ERROR_CODE, FILE_TOO_BIG_ERROR_TEXT, 
    PDF_PROCESSING_ERROR_CODE, PDF_PROCESSING_ERROR_TEXT,
    TIMEOUT_ERROR_CODE, TIMEOUT_ERROR_TEXT,
    RATE_LIMIT_ERROR_CODE, RATE_LIMIT_ERROR_TEXT,
    GENERAL_ERROR_CODE, GENERAL_ERROR_MESSAGE
)
from pdf_processing.validation import validate_file_size, validate_file_type
from fastapi import UploadFile, HTTPException
from clients.gemini_client import gemini_request, RateLimitError
from .logger import logger


async def validate_file(file: UploadFile):
    logger.info(f"Validating file: {file.filename}")
    # Can also read in a loop if MAX_FILE_SIZE is too big
    chunk = await file.read(MAX_FILE_SIZE+1)
    await file.seek(0)
    if not validate_file_size(chunk, MAX_FILE_SIZE):
        logger.warning(f"Max file size ({MAX_FILE_SIZE} Bytes) exceeded for file: {file.filename}")
        raise HTTPException(status_code=FILE_TOO_BIG_ERROR_CODE, detail=FILE_TOO_BIG_ERROR_TEXT)

    if not validate_file_type(chunk):
        logger.warning(f"Invalid file type for file: {file.filename}")
        raise HTTPException(status_code=FILE_NOT_VALID_PDF_ERROR_CODE, detail=FILE_NOT_VALID_PDF_ERROR_TEXT)
    
    logger.info(f"File validation passed for file: {file.filename}")
    return chunk

async def extract_info_from_pdf(contents: bytes) -> tuple:
    try:
        logger.info("Starting PDF extraction")
        extracted_text, page_count = await to_thread(extract_info, contents)
        logger.info(f"Successfully extracted PDF Info")
    except Exception as e:
        logger.error(f"Error extracting PDF info: {str(e)}")
        raise HTTPException(status_code=PDF_PROCESSING_ERROR_CODE, detail=f"{PDF_PROCESSING_ERROR_TEXT}: {str(e)}")
    return extracted_text, page_count

async def get_ai_response(pdf_content: str, user_message: str) -> str:
    context = "respond to this user's message based on the provided text"
    prompt = [context, user_message, pdf_content]
    try:
        logger.info("Sending prompt")
        response = await wait_for(gemini_request(prompt), timeout = TIMEOUT_TIME)
        logger.info("Received response")
    except TimeoutError:
        logger.warning("Request timed out")
        raise HTTPException(status_code=TIMEOUT_ERROR_CODE, detail=TIMEOUT_ERROR_TEXT)
    except RateLimitError:
        logger.warning("Gemini API rate limit exceeded")
        raise HTTPException(status_code=RATE_LIMIT_ERROR_CODE, detail=RATE_LIMIT_ERROR_TEXT)
    except Exception as e:
        logger.error(f"Unexpected error in get_ai_response: {str(e)}")
        raise HTTPException(status_code=GENERAL_ERROR_CODE, detail=f"{GENERAL_ERROR_MESSAGE}: {str(e)}")
    else:
        return response.text
