from fastapi import APIRouter, Depends, Security, HTTPException
from fastapi.security import APIKeyCookie
from fastapi_sso import GoogleSSO
from jose import jwt
from datetime import datetime, timedelta

from pydantic import BaseModel
from starlette.config import Config
from starlette.requests import Request
from starlette.responses import RedirectResponse

from models.Blacklist import add_blacklist, find_blacklist
from models.User import create_or_update_user

router = APIRouter(prefix='/login', tags=['auth'])
config = Config('.env')

SECRET_KEY = config('SECRET_KEY')
FRONTEND_URL = config('FRONTEND_URL')
BASE_URL = config.get('BASE_URL')

google_sso = GoogleSSO(
    config.get('GOOGLE_CLIENT_ID'),
    config.get('GOOGLE_CLIENT_SECRET'),
    f'{BASE_URL}/login/google/callback')


class Session(BaseModel):
    name: str
    email: str
    id: int
    profile: str


async def get_logged_user(cookie: str = Security(APIKeyCookie(name="token")), token: str = Security(APIKeyCookie(name="token"))) -> Session:
    """Get user's JWT stored in cookie 'token', parse it and return the user's OpenID."""
    try:
        blacklisted = await find_blacklist(token)
        if blacklisted:
            raise HTTPException(status_code=403, detail='Blacklisted')
        claims = jwt.decode(cookie, key=SECRET_KEY, algorithms=["HS256"])
        return Session(**claims["pld"])
    except HTTPException as error:
        raise error
    except Exception as error:
        raise HTTPException(status_code=401, detail="Invalid authentication credentials") from error


@router.get('/username')
async def username(user: Session = Depends(get_logged_user)):
    return {
        'name': user.name,
        'email': user.email,
        'id': user.id,
        'profile': user.profile
    }

@router.get('/logout')
async def logout(token: str = Security(APIKeyCookie(name="token"))):
    await add_blacklist(token)

    return True


@router.get("/google", include_in_schema=False)
async def login_google(request: Request):
    with google_sso:
        return await google_sso.get_login_redirect()


@router.get("/google/callback", include_in_schema=False)
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

        token = jwt.encode({"pld": Session(**userdata).__dict__, "exp": exp, "sub": user.email}, key=SECRET_KEY,
                           algorithm="HS256")
        response = RedirectResponse(url=FRONTEND_URL, status_code=302)
        response.set_cookie(
            key="token", value=token, httponly=True
        )

        return response
