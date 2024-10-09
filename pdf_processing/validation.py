import fitz

def validate_file_type(content: bytes) -> bool:
    try:
        with fitz.open(stream=content, filetype="pdf") as doc:
            pass
    except Exception:
        return False
    return True

def validate_file_size(chunk: bytes, max_size: int) -> bool:
    if len(chunk) > max_size:
        return False
    return True
