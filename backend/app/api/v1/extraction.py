from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.schemas.extraction import ExtractionRunResponse, RequirementsResponse
from app.services.extraction_service import ExtractionService
from app.tasks.extraction_tasks import extract_requirements_task

router = APIRouter()

@router.post("/{case_id}/extract", response_model=ExtractionRunResponse)
async def start_extraction(
    case_id: int,
    db: Session = Depends(get_db)
):
    """Start async extraction process"""
    service = ExtractionService(db)
    run = service.create_extraction_run(case_id)
    if not run:
        raise HTTPException(status_code=404, detail="Case not found or no transcript available")
    
    # Trigger async task
    extract_requirements_task.delay(run.id)
    
    return run

@router.get("/cases/runs/{run_id}", response_model=ExtractionRunResponse)
async def get_extraction_run(
    run_id: int,
    db: Session = Depends(get_db)
):
    """Get extraction run status"""
    service = ExtractionService(db)
    run = service.get_extraction_run(run_id)
    if not run:
        raise HTTPException(status_code=404, detail="Extraction run not found")
    return run

@router.get("/{case_id}/requirements", response_model=RequirementsResponse)
async def get_requirements(
    case_id: int,
    run_id: int = Query(None),
    db: Session = Depends(get_db)
):
    """Get extracted requirements for a case"""
    service = ExtractionService(db)
    requirements = service.get_requirements(case_id, run_id)
    if not requirements:
        raise HTTPException(status_code=404, detail="Requirements not found")
    return requirements

@router.put("/{case_id}/requirements", response_model=RequirementsResponse)
async def update_requirements(
    case_id: int,
    requirements_data: dict,
    run_id: int = Query(None),
    db: Session = Depends(get_db)
):
    """Update extracted requirements (user edits)"""
    service = ExtractionService(db)
    requirements = service.update_requirements(case_id, run_id, requirements_data)
    if not requirements:
        raise HTTPException(status_code=404, detail="Requirements not found")
    return requirements

