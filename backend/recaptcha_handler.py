from backend.config import RECAPTCHA_SECRET_KEY

from fastapi import HTTPException
import httpx


async def recaptcha_handler(recaptcha_response: str) -> bool:
    url = 'https://www.google.com/recaptcha/api/siteverify'
    data = {
        'secret': RECAPTCHA_SECRET_KEY,
        'response': recaptcha_response,
    }

    async with httpx.AsyncClient() as client:
        response = await client.post(url, data=data)
    result = response.json()

    if not result.get('success', False):
        raise HTTPException(status_code=500, detail='reCAPTCHA verification failed')
    return True
