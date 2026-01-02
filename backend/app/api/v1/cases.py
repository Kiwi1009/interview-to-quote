from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.core.database import get_db
from app.models.case import Case
from app.schemas.case import CaseCreate, CaseResponse, CaseUpdate
from app.services.case_service import CaseService

router = APIRouter()

@router.post("", response_model=CaseResponse, status_code=201)
async def create_case(
    case_data: CaseCreate,
    db: Session = Depends(get_db)
):
    """Create a new case"""
    service = CaseService(db)
    return service.create_case(case_data)

@router.get("", response_model=List[CaseResponse])
async def list_cases(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """List all cases"""
    service = CaseService(db)
    return service.list_cases(skip=skip, limit=limit)

@router.get("/{case_id}", response_model=CaseResponse)
async def get_case(
    case_id: int,
    db: Session = Depends(get_db)
):
    """Get a case by ID"""
    service = CaseService(db)
    case = service.get_case(case_id)
    if not case:
        raise HTTPException(status_code=404, detail="Case not found")
    return case

@router.put("/{case_id}", response_model=CaseResponse)
async def update_case(
    case_id: int,
    case_data: CaseUpdate,
    db: Session = Depends(get_db)
):
    """Update a case"""
    service = CaseService(db)
    case = service.update_case(case_id, case_data)
    if not case:
        raise HTTPException(status_code=404, detail="Case not found")
    return case

