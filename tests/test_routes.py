from fastapi.testclient import TestClient
from app.main import app
from app.db import database
from app.config import FILE_NOT_VALID_PDF_ERROR_CODE, FILE_TOO_BIG_ERROR_CODE, FILE_NOT_VALID_PDF_ERROR_TEXT, FILE_TOO_BIG_ERROR_TEXT
from .config import NON_PDF, TEXT_ONLY_BIG_PDF, TEXT_ONLY_SMALL_PDF, EMPTY_PDF, CORRUPT_PDF
from .utils import get_test_file_path, is_valid_uuid
import pytest

client = TestClient(app)

def test_non_pdf_file():
    file_path = get_test_file_path(NON_PDF)
    with open(file_path, "rb") as non_pdf_file:
        files = {"file": (NON_PDF, non_pdf_file)}
        response = client.post("/v1/pdf", files=files)
    assert response.status_code == FILE_NOT_VALID_PDF_ERROR_CODE
    assert response.headers["content-type"] == "application/json"
    response_json = response.json()
    assert "detail" in response_json
    assert response_json["detail"] == FILE_NOT_VALID_PDF_ERROR_TEXT

def test_empty_pdf_file():
    file_path = get_test_file_path(EMPTY_PDF)
    with open(file_path, "rb") as empty_pdf_file:
        files = {"file": (EMPTY_PDF, empty_pdf_file)}
        response = client.post("/v1/pdf", files=files)
    assert response.status_code == FILE_NOT_VALID_PDF_ERROR_CODE
    assert response.headers["content-type"] == "application/json"
    response_json = response.json()
    assert "detail" in response_json
    assert response_json["detail"] == FILE_NOT_VALID_PDF_ERROR_TEXT

def test_corrupt_pdf_file():
    file_path = get_test_file_path(CORRUPT_PDF)
    with open(file_path, "rb") as corrupt_pdf_file:
        files = {"file": (CORRUPT_PDF, corrupt_pdf_file)}
        response = client.post("/v1/pdf", files=files)
    assert response.status_code == FILE_NOT_VALID_PDF_ERROR_CODE
    assert response.headers["content-type"] == "application/json"
    response_json = response.json()
    assert "detail" in response_json
    assert response_json["detail"] == FILE_NOT_VALID_PDF_ERROR_TEXT

def test_text_only_big_pdf_file():
    file_path = get_test_file_path(TEXT_ONLY_BIG_PDF)
    with open(file_path, "rb") as text_only_big:
        files = {"file": (TEXT_ONLY_BIG_PDF, text_only_big)}
        response = client.post("/v1/pdf", files=files)
    assert response.status_code == FILE_TOO_BIG_ERROR_CODE
    assert response.headers["content-type"] == "application/json"
    response_json = response.json()
    assert "detail" in response_json
    assert response_json["detail"] == FILE_TOO_BIG_ERROR_TEXT
'''
@pytest.mark.asyncio
async def test_text_only_small_pdf_file():
    await database.connect()
    file_path = get_test_file_path(TEXT_ONLY_SMALL_PDF)
    with open(file_path, "rb") as text_only_small:
        files = {"file": (TEXT_ONLY_SMALL_PDF, text_only_small)}
        response = client.post("/v1/pdf", files=files)
    assert response.status_code == 200
    assert response.headers["content-type"] == "application/json"
    response_json = response.json()
    assert "pdf_id" in response_json
    assert is_valid_uuid(response_json["pdf_id"])
'''
