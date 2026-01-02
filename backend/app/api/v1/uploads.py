from fastapi import APIRouter, Depends, UploadFile, File, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.core.database import get_db
from app.schemas.upload import UploadResponse
from app.services.upload_service import UploadService

router = APIRouter()

@router.post("/{case_id}/uploads", response_model=UploadResponse, status_code=201)
async def upload_file(
    case_id: int,
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    """Upload a transcript or photo file"""
    service = UploadService(db)
    upload = await service.upload_file(case_id, file)
    if not upload:
        raise HTTPException(status_code=404, detail="Case not found")
    return upload

@router.get("/{case_id}/uploads", response_model=List[UploadResponse])
async def list_uploads(
    case_id: int,
    db: Session = Depends(get_db)
):
    """List all uploads for a case"""
    service = UploadService(db)
    return service.list_uploads(case_id)

