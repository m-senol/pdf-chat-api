from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import JSONResponse
from uuid import uuid4

MAX_FILE_SIZE = 100*1024
CHUNK_SIZE    = 1024

app = FastAPI()

async def validate_file_type(file: UploadFile):
    if not file.filename.endswith('.pdf'):
        raise HTTPException(status_code=400, detail="Invalid file type!")

async def validate_file_size(file: UploadFile):
    size = 0
    try:
        while True:
            chunk = await file.read(CHUNK_SIZE)
            if not chunk:
                break
            size+=len(chunk)
            if size > MAX_FILE_SIZE:
                raise HTTPException(status_code=400, detail="File size exceeds size limit!")
    finally:
        file.seek(0)

async def validate_file(file: UploadFile):
    await validate_file_type(file)
    await validate_file_size(file)

@app.post("/v1/pdf")
async def upload_pdf(file: UploadFile = File(...)):
    await validate_file(file)
    pdf_id = str(uuid4())
    return JSONResponse(content={"pdf_id": pdf_id})
