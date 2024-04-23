from fastapi import APIRouter, Depends, Security, HTTPException
from fastapi.security import APIKeyCookie
from fastapi_sso import GoogleSSO, NaverSSO, GithubSSO
from jose import jwt
from datetime import datetime, timedelta

from pydantic import BaseModel
from starlette.requests import Request
from starlette.responses import RedirectResponse, Response

from backend.config import GOOGLE_CLIENT_ID, GOOGLE_CLIENT_SECRET, BASE_URL, SECRET_KEY, FRONTEND_URL, NAVER_CLIENT_ID, \
    NAVER_CLIENT_SECRET, GITHUB_CLIENT_ID, GITHUB_CLIENT_SECRET
from backend.models.Blacklist import add_blacklist, find_blacklist
from backend.models.User import create_or_update_user
from backend.models.database import UserRole

router = APIRouter(prefix='/login', tags=['auth'])

google_sso = GoogleSSO(
    GOOGLE_CLIENT_ID,
    GOOGLE_CLIENT_SECRET,
    f'{BASE_URL}/login/google/callback'
)
naver_sso = NaverSSO(
    client_id=NAVER_CLIENT_ID,
    client_secret=NAVER_CLIENT_SECRET,
    redirect_uri=f'{BASE_URL}/login/naver/callback',
    allow_insecure_http=True
)

github_sso = GithubSSO(
    GITHUB_CLIENT_ID,
    GITHUB_CLIENT_SECRET,
    f'{BASE_URL}/login/github/callback'
)


class Session(BaseModel):
    name: str
    email: str
    id: int
    profile: str
    role: int


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
        'profile': user.profile,
        'role': user.role
    }


@router.get('/logout')
async def logout(token: str = Security(APIKeyCookie(name="token"))):
    await add_blacklist(token)

    response = Response()
    response.delete_cookie('token')

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


@router.get("/github", include_in_schema=False)
async def login_github(request: Request):
    with github_sso:
        return await github_sso.get_login_redirect()


@router.get("/github/callback", include_in_schema=False)
async def login_github_callback(request: Request):
    with github_sso:
        user = await github_sso.verify_and_process(request)
        if not user:
            raise HTTPException(status_code=401, detail="Authentication failed")

        userdata = await create_or_update_user(
            vendor="github",
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


@router.get("/naver", include_in_schema=False)
async def login_naver(request: Request):
    with naver_sso:
        return await naver_sso.get_login_redirect()


@router.get("/naver/callback", include_in_schema=False)
async def login_naver_callback(request: Request):
    with naver_sso:
        user = await naver_sso.verify_and_process(request, params={"client_secret": NAVER_CLIENT_SECRET})
        if not user:
            raise HTTPException(status_code=401, detail="Authentication failed")
        userdata = await create_or_update_user(
            vendor="naver",
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
