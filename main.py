from datetime import datetime, timedelta
from fastapi import FastAPI, HTTPException, Security, Depends
from fastapi.openapi.models import Response
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer, APIKeyCookie
from fastapi_sso import OpenID
from fastapi_sso.sso.google import GoogleSSO
from pydantic import BaseModel, Extra
from starlette.config import Config
from starlette.requests import Request
from jose import jwt
from starlette.responses import RedirectResponse

from models.User import create_or_update_user, User
from models.database import create_tables

app = FastAPI()
security = HTTPBearer()

config = Config('.env')
SECRET_KEY = config('SECRET_KEY')

google_sso = GoogleSSO(
    config.get('GOOGLE_CLIENT_ID'),
    config.get('GOOGLE_CLIENT_SECRET'),
    f'{config.get('BASE_URL')}/login/google/callback')


class Session(BaseModel):
    name: str
    email: str
    id: int
    profile: str


async def get_logged_user(cookie: str = Security(APIKeyCookie(name="token"))) -> Session:
    """Get user's JWT stored in cookie 'token', parse it and return the user's OpenID."""
    try:
        claims = jwt.decode(cookie, key=SECRET_KEY, algorithms=["HS256"])
        return Session(**claims["pld"])
    except Exception as error:
        raise HTTPException(status_code=401, detail="Invalid authentication credentials") from error


@app.on_event('startup')
async def startup():
    await create_tables()


@app.get('/username')
async def username(user: Session = Depends(get_logged_user)):
    return {
        'name': user.name,
        'email': user.email,
        'id': user.id,
        'profile': user.profile
    }

@app.get("/login/google")
async def login_google(request: Request):
    with google_sso:
        return await google_sso.get_login_redirect()


@app.get("/login/google/callback")
async def login_google_callback(request: Request):
    with google_sso:
        user = await google_sso.verify_and_process(request)
        if not user:
            raise HTTPException(status_code=401, detail="Authentication failed")
        userdata = await create_or_update_user(
            vendor="google",
            token=user.id,  # `user.id`는 Google에서 제공하는 사용자 ID입니다.
            profile=user.picture,  # 사용자의 프로필 이미지 URL입니다.
            name=user.display_name,
            email=user.email
        )
        exp = datetime.now() + timedelta(hours=1)

        token = jwt.encode({"pld": Session(**userdata).__dict__, "exp": exp, "sub": user.email}, key=SECRET_KEY, algorithm="HS256")
        response = RedirectResponse(url="/", status_code=302)
        response.set_cookie(
            key="token", value=token, httponly=True
        )

        return response

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
