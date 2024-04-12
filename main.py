from fastapi import FastAPI
from fastapi.security import HTTPBearer
from fastapi_utilities import repeat_at
from slowapi import _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
from starlette.config import Config

import router_auth
import router_correction
from models.Blacklist import delete_blacklist
from models.database import create_tables
from rate_limiter import limiter

app = FastAPI()
security = HTTPBearer()
config = Config('.env')

app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

app.include_router(router_auth.router)
app.include_router(router_correction.router)


@app.on_event('startup')
async def startup():
    await create_tables()


@app.on_event('startup')
@repeat_at(cron="0 0/12 * * *")
async def blacklist_cron():
    await delete_blacklist()


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
