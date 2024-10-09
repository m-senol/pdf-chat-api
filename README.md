PDF CHAT API
============

# Introduction

This is a FastAPI-based API that allows users to upload PDF files, and interact with the content using Google's Gemini API for advanced natural language processing.

The PDF Chat API provides the following functionality:

- **PDF Upload**: Users can upload PDFs, which are processed to extract their text content and metadata. The extracted information is stored in a PostgreSQL database.

- **Chat with PDF**: Users can ask questions about the content of the uploaded PDFs, and the API will use Google's Gemini API to generate a context-aware response based on the PDF's content.

## Overview
- **FastAPI:** The core web framework used for building the API.
- **Google Generative AI:** Integration with Google's Gemini API for generating AI-based responses.
- **PostgreSQL:** Storing extracted PDF content and metadata.
- **Async Operations:** Utilizes asynchronous database queries and PDF processing for non-blocking operations.
- **Comprehensive Error Handling:** Manages file type validation, timeouts, rate limits, and API errors.

# Setup

## 1. Prerequisites
- Python 3.12.7+
- PostgreSQL
- Google Gemini API Key

## 2. Clone The Repository
```bash
git clone "https://github.com/m-senol/pdf-chat-api.git"
cd pdf-chat-api
```
## 3. Set Up Environment Variables
Create a ``.env`` file in the project root and configure the necessary environment variables:

```
API_KEY=<api_key>
DATABASE_URL=postgresql://<username>:<password>@<host><port>/<database_name>
```

## 4. Install Dependencies
```bash
pip install -r requirements.txt
```

# Endpoints

## Upload
- **Endpoint:**  ``/v1/pdf``
- **Method:** ``POST``
- **Despcription:** Endpoint for uploading and registering a PDF

- **Input**
    - **Description:** Multipart form data containing the PDF file
    - **Example**
        ```bash
        curl -X POST "http://localhost:8000/v1/pdf" \
        -F "file=@/path/to/your/pdf/file.pdf"
        ```
- **Output**
    - **Description:** JSON response with the generated PDF ID
    - **Example**
        ```json
        {
            "pdf_id": "unique_pdf_identifier"
        }
        ```

## Chat
- **Endpoint:**  ``/v1/chat/{pdf_id}``
- **Method:** ``POST``
- **Despcription:** Endpoint for interacting with a specific PDF

- **Input**
    - **Description:** JSON body containing the user's message
    - **Example**
        ```bash
        curl -X POST "http://localhost:8000/v1/chat/pdf_id" \
        -H "Content-Type: application/json" \
        --data '{"message": "What is this about?"}'
        ```
- **Output**
    - **Description:** JSON response with the AI-generated answer
    - **Example**
        ```json
        {
        "response": "The main topic of this PDF is ."
        }
        ```

# Tests
Unit tests are implemented using pytest with asynchronous support.

Execute the following command to run the test:
```bash
pytest
```
