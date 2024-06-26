from datetime import datetime
from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException
from starlette.requests import Request
from pydantic import BaseModel

from backend.models.Notification import get_latest_notification as get_latest_notification_model, get_notifications, \
    get_total_notification_count, create_or_update_notification
from backend.models.database import UserRole
from backend.rate_limiter import limiter
from backend.router_auth import Session, get_logged_user

router = APIRouter(prefix="/notification", tags=["notification"])


class NotificationResponse(BaseModel):
    id: int
    user_id: int
    content: str
    created_at: datetime
    updated_at: datetime


class NotificationRequest(BaseModel):
    id: Optional[int] = 0
    content: str


class SizeResponse(BaseModel):
    size: int
    pages: int


@router.get("/latest", response_model=NotificationResponse)
@limiter.limit("30/second")
async def get_latest_notification(request: Request):
    data = await get_latest_notification_model()
    result = data[0]
    return NotificationResponse(
        id=result.id,
        user_id=result.user_id,
        content=result.content,
        created_at=result.created_at,
        updated_at=result.updated_at
    )


@router.get("/list/{page_no}", response_model=List[NotificationResponse])
@limiter.limit("5/second")
async def list_corrections(request: Request, page_no: int) -> List[NotificationResponse]:
    if page_no < 1:
        raise HTTPException(status_code=400, detail="Page number must be greater than 0")
    results = await get_notifications(page_no)
    return [NotificationResponse(
        id=entries.id,
        user_id=entries.user_id,
        content=entries.content,
        created_at=entries.created_at,
        updated_at=entries.updated_at,
    ) for entries in results]


@router.get("/size", response_model=SizeResponse)
@limiter.limit("30/second")
async def get_size(request: Request):
    total_size = await get_total_notification_count()
    pages = (total_size + 49) // 50
    return SizeResponse(size=total_size, pages=pages)


@router.post("/create", response_model=NotificationResponse)
@limiter.limit("5/second")
async def create_notification(request: Request, data: NotificationRequest, user: Session = Depends(get_logged_user)):
    if user.role == UserRole.USER:
        raise HTTPException(status_code=403, detail="Only Admin or Moderator can create notifications")
    results = await create_or_update_notification(data.id, data.content, user.id)

    return NotificationResponse(
        id=results.id,
        user_id=results.user_id,
        content=results.content,
        created_at=results.created_at,
        updated_at=results.updated_at
    )