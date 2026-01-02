from sqlalchemy.orm import Session
from typing import Optional, Dict, Any
from app.models.case import Case
from app.models.extraction_run import ExtractionRun, ExtractionStatus
from app.models.extracted_requirement import ExtractedRequirement
from app.models.evidence import Evidence
from app.models.upload import Upload, UploadType

class ExtractionService:
    def __init__(self, db: Session):
        self.db = db
    
    def create_extraction_run(self, case_id: int) -> Optional[ExtractionRun]:
        case = self.db.query(Case).filter(Case.id == case_id).first()
        if not case:
            return None
        
        # Check if transcript exists
        transcript = self.db.query(Upload).filter(
            Upload.case_id == case_id,
            Upload.type == UploadType.TRANSCRIPT
        ).first()
        if not transcript:
            return None
        
        # Get next version number
        last_run = self.db.query(ExtractionRun).filter(
            ExtractionRun.case_id == case_id
        ).order_by(ExtractionRun.version.desc()).first()
        version = (last_run.version + 1) if last_run else 1
        
        run = ExtractionRun(
            case_id=case_id,
            version=version,
            status=ExtractionStatus.PENDING
        )
        self.db.add(run)
        self.db.commit()
        self.db.refresh(run)
        return run
    
    def get_extraction_run(self, run_id: int) -> Optional[ExtractionRun]:
        return self.db.query(ExtractionRun).filter(ExtractionRun.id == run_id).first()
    
    def get_requirements(self, case_id: int, run_id: Optional[int] = None) -> Optional[Dict[str, Any]]:
        if run_id:
            run = self.db.query(ExtractionRun).filter(
                ExtractionRun.id == run_id,
                ExtractionRun.case_id == case_id
            ).first()
        else:
            run = self.db.query(ExtractionRun).filter(
                ExtractionRun.case_id == case_id
            ).order_by(ExtractionRun.version.desc()).first()
        
        if not run:
            return None
        
        req = self.db.query(ExtractedRequirement).filter(
            ExtractedRequirement.run_id == run.id
        ).first()
        
        if not req:
            return None
        
        # Get evidence
        evidence_list = self.db.query(Evidence).filter(
            Evidence.run_id == run.id
        ).all()
        
        from app.schemas.extraction import RequirementsResponse, EvidenceResponse
        
        return RequirementsResponse(
            run_id=run.id,
            jsonb_data=req.jsonb_data,
            confidence=req.confidence,
            evidence=[EvidenceResponse(
                field_path=e.field_path,
                segment_idx=e.segment_idx,
                snippet=e.snippet,
                start_char=e.start_char,
                end_char=e.end_char
            ) for e in evidence_list],
            created_at=req.created_at
        )
    
    def update_requirements(self, case_id: int, run_id: Optional[int], requirements_data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        if run_id:
            run = self.db.query(ExtractionRun).filter(
                ExtractionRun.id == run_id,
                ExtractionRun.case_id == case_id
            ).first()
        else:
            run = self.db.query(ExtractionRun).filter(
                ExtractionRun.case_id == case_id
            ).order_by(ExtractionRun.version.desc()).first()
        
        if not run:
            return None
        
        req = self.db.query(ExtractedRequirement).filter(
            ExtractedRequirement.run_id == run.id
        ).first()
        
        if req:
            req.jsonb_data = requirements_data
        else:
            req = ExtractedRequirement(
                run_id=run.id,
                jsonb_data=requirements_data
            )
            self.db.add(req)
        
        self.db.commit()
        self.db.refresh(req)
        
        # Return updated requirements
        return self.get_requirements(case_id, run_id)

