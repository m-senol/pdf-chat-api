import google.generativeai as genai
from google.generativeai.types.generation_types import GenerateContentResponse
from .config import API_KEY
from google.api_core.exceptions import ResourceExhausted

genai.configure(api_key=API_KEY)
model = genai.GenerativeModel("gemini-1.5-flash")

class RateLimitError(Exception):
    pass

async def gemini_request(prompt) -> GenerateContentResponse: 
    try:
        response =  await model.generate_content_async(prompt)
    except ResourceExhausted:
        raise RateLimitError()
    else:
        return response
