from datetime import datetime
from typing import List

from fastapi import APIRouter, Depends, HTTPException
from starlette.requests import Request
from pydantic import BaseModel

from backend.models.Dataset import get_datasets, create_dataset, get_total_datasets_count
from backend.models.database import DatasetStatus
from backend.rate_limiter import limiter
from backend.router_auth import Session, get_logged_user

router = APIRouter(prefix="/dataset", tags=["dataset"])


class CorrectionRequest(BaseModel):
    text: str
    correction: str
    memo: str


class CorrectionResponse(BaseModel):
    id: int
    text: str
    correction: str
    memo: str
    status: int
    created_at: datetime
    updated_at: datetime
    user: Session


class SizeResponse(BaseModel):
    size: int
    pages: int


@router.get("/list/{page_no}", response_model=List[CorrectionResponse])
@limiter.limit("5/second")
async def list_corrections(request: Request, page_no: int) -> List[CorrectionResponse]:
    if page_no < 1:
        raise HTTPException(status_code=400, detail="Page number must be greater than 0")
    results = await get_datasets(page_no)
    return [CorrectionResponse(
        id=entries.id,
        text=entries.text,
        correction=entries.corrected,
        memo=entries.memo or "",
        status=int(entries.status),
        created_at=entries.created_at,
        updated_at=entries.updated_at,
        user=Session(
            id=entries.user.id,
            name=entries.user.name,
            email=entries.user.email,
            profile=entries.user.profile,
            role=entries.user.role
        )
    ) for entries in results]


@router.post("/create", response_model=CorrectionResponse)
@limiter.limit("5/second")
async def create_correction(request: Request, data: CorrectionRequest, user: Session = Depends(get_logged_user)):
    await create_dataset(user.id, data.text, data.correction, data.memo)
    return CorrectionResponse(
        id=0,
        text=data.text,
        correction=data.correction,
        memo=data.memo,
        status=int(DatasetStatus.PENDING),
        created_at=datetime.now(),
        updated_at=datetime.now(),
        user=user
    )


@router.get("/size", response_model=SizeResponse)
@limiter.limit("30/second")
async def get_size(request: Request):
    total_size = await get_total_datasets_count()
    pages = (total_size + 49) // 50
    return SizeResponse(size=total_size, pages=pages)