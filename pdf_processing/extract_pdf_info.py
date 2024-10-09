from fitz import open
from re import sub
from .config import REGEX_HTML, REGEX_URL


def remove_html_tags(text: str) -> str:
    return sub(REGEX_HTML, '', text)

def remove_urls(text: str) -> str:
    return sub(REGEX_URL, '', text)

def text_preprocessing(text: str) -> str:
    processed_text = remove_urls(text.lower())
    processed_text = remove_html_tags(processed_text)
    return processed_text

def extract_text(pdf_document):
    text = ""
    for page_num in range(pdf_document.page_count):
        page = pdf_document.load_page(page_num)
        text += page.get_text("text")
    return text_preprocessing(text)

def extract_page_num(pdf_document):
    return pdf_document.page_count

def extract_info(contents: bytes) -> tuple:
    with open(stream=contents, filetype="pdf") as pdf_document:
        text = extract_text(pdf_document)
        page_num = extract_page_num(pdf_document)
    return text, page_num
