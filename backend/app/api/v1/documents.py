from fastapi import APIRouter, Depends, HTTPException, Query, Response
from sqlalchemy.orm import Session
from typing import List
from app.core.database import get_db
from app.schemas.document import DocumentResponse
from app.services.document_service import DocumentService
from app.tasks.document_tasks import generate_documents_task

router = APIRouter()

@router.post("/{case_id}/documents")
async def generate_documents(
    case_id: int,
    run_id: int = Query(None),
    types: str = Query("spec,report,quote"),
    formats: str = Query("docx,pdf"),
    db: Session = Depends(get_db)
):
    """Generate documents (async)"""
    doc_types = [t.strip() for t in types.split(",")]
    doc_formats = [f.strip() for f in formats.split(",")]
    
    # Trigger async task
    task = generate_documents_task.delay(case_id, run_id, doc_types, doc_formats)
    
    # Return pending status
    return {"task_id": task.id, "status": "pending"}

@router.get("/{case_id}/documents", response_model=List[DocumentResponse])
async def list_documents(
    case_id: int,
    run_id: int = Query(None),
    db: Session = Depends(get_db)
):
    """List documents for a case"""
    service = DocumentService(db)
    return service.list_documents(case_id, run_id)

@router.get("/documents/{doc_id}/download")
async def download_document(
    doc_id: int,
    db: Session = Depends(get_db)
):
    """Download a document file"""
    service = DocumentService(db)
    doc_path = service.get_document_path(doc_id)
    if not doc_path:
        raise HTTPException(status_code=404, detail="Document not found")
    
    import os
    from fastapi.responses import FileResponse
    
    if not os.path.exists(doc_path):
        raise HTTPException(status_code=404, detail="Document file not found")
    
    return FileResponse(
        doc_path,
        media_type="application/octet-stream",
        filename=os.path.basename(doc_path)
    )

