from os import getenv
from dotenv import load_dotenv

load_dotenv()


DATABASE_URL = getenv("DATABASE_URL")


MAX_FILE_SIZE = 100*1024 # 100 kB


FILE_TOO_BIG_ERROR_CODE = 400
FILE_TOO_BIG_ERROR_TEXT = "File size exceeds size limit!"

FILE_NOT_VALID_PDF_ERROR_CODE = 400
FILE_NOT_VALID_PDF_ERROR_TEXT = "Invalid file!"

PDF_PROCESSING_ERROR_CODE = 400
PDF_PROCESSING_ERROR_TEXT = "Error processing PDF!"

PDF_NOT_FOUND_ERROR_CODE = 404
PDF_NOT_FOUND_ERROR_TEXT = "PDF not found!"

TIMEOUT_ERROR_CODE = 408
TIMEOUT_ERROR_TEXT = "The request to the Gemini API timed out. Please try again later."

RATE_LIMIT_ERROR_CODE = 429
RATE_LIMIT_ERROR_TEXT = "Rate limit exceeded. Please try again later."

GENERAL_ERROR_CODE = 500
GENERAL_ERROR_MESSAGE = "An unexpected error occurred!"

TIMEOUT_TIME = 10
