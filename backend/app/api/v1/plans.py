from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List
from app.core.database import get_db
from app.schemas.plan import PlanResponse, PlanUpdate
from app.services.plan_service import PlanService

router = APIRouter()

@router.post("/{case_id}/generate-plans", response_model=List[PlanResponse])
async def generate_plans(
    case_id: int,
    run_id: int = Query(None),
    db: Session = Depends(get_db)
):
    """Generate 3 plan options (P1/P2/P3)"""
    service = PlanService(db)
    plans = service.generate_plans(case_id, run_id)
    if not plans:
        raise HTTPException(status_code=404, detail="Case or requirements not found")
    return plans

@router.get("/{case_id}/plans", response_model=List[PlanResponse])
async def list_plans(
    case_id: int,
    run_id: int = Query(None),
    db: Session = Depends(get_db)
):
    """List plans for a case"""
    service = PlanService(db)
    return service.list_plans(case_id, run_id)

@router.put("/plans/{plan_id}", response_model=PlanResponse)
async def update_plan(
    plan_id: int,
    plan_data: PlanUpdate,
    db: Session = Depends(get_db)
):
    """Update plan assumptions and pricing overrides"""
    service = PlanService(db)
    plan = service.update_plan(plan_id, plan_data)
    if not plan:
        raise HTTPException(status_code=404, detail="Plan not found")
    return plan

