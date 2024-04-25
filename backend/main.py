from fastapi import FastAPI
from fastapi.security import HTTPBearer
from fastapi_utilities import repeat_at
from slowapi import _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
from fastapi.middleware.cors import CORSMiddleware

from backend import router_auth, router_correction, router_dataset, router_notification
from backend.config import FRONTEND_URL, IS_PRODUCTION
from backend.rate_limiter import limiter
from backend.models.Blacklist import delete_blacklist

app = FastAPI(
    docs_url=None if IS_PRODUCTION else "/docs",
    redoc_url=None if IS_PRODUCTION else "/redoc"
)
security = HTTPBearer()

app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

app.include_router(router_auth.router)
app.include_router(router_correction.router)
app.include_router(router_dataset.router)
app.include_router(router_notification.router)


origins = [
    FRONTEND_URL
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)


@app.on_event('startup')
@repeat_at(cron="0 0/12 * * *")
async def blacklist_cron():
    await delete_blacklist()


@app.get('/health')
async def health():
    return {'status': 'ok'}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
