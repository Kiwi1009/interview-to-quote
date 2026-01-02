from app.celery_app import celery_app
from app.core.database import SessionLocal
from app.models.extraction_run import ExtractionRun, ExtractionStatus
from app.models.extracted_requirement import ExtractedRequirement
from app.models.evidence import Evidence
from app.models.upload import Upload, UploadType
from app.models.transcript_segment import TranscriptSegment
from app.services.llm_service import LLMService
from app.validators.requirements_validator import RequirementsValidator
from datetime import datetime

@celery_app.task
def extract_requirements_task(run_id: int):
    """Async task to extract requirements from transcript"""
    db = SessionLocal()
    try:
        run = db.query(ExtractionRun).filter(ExtractionRun.id == run_id).first()
        if not run:
            return
        
        run.status = ExtractionStatus.RUNNING
        db.commit()
        
        # Get transcript
        transcript_upload = db.query(Upload).filter(
            Upload.case_id == run.case_id,
            Upload.type == UploadType.TRANSCRIPT
        ).first()
        
        if not transcript_upload:
            run.status = ExtractionStatus.FAILED
            db.commit()
            return
        
        # Read transcript
        with open(transcript_upload.path, 'r', encoding='utf-8') as f:
            transcript_text = f.read()
        
        # Get segments
        segments = db.query(TranscriptSegment).filter(
            TranscriptSegment.case_id == run.case_id
        ).order_by(TranscriptSegment.idx).all()
        
        # Extract using LLM
        llm_service = LLMService()
        result = llm_service.extract_requirements(transcript_text, segments)
        
        # Validate requirements
        validator = RequirementsValidator()
        validation = validator.validate(result["requirements"])
        
        # Update open_questions with missing fields
        if validation["missing_fields"]:
            if "open_questions" not in result["requirements"]:
                result["requirements"]["open_questions"] = []
            result["requirements"]["open_questions"].extend(validation["open_questions"])
        
        # Save extracted requirements
        extracted_req = ExtractedRequirement(
            run_id=run.id,
            jsonb_data=result["requirements"],
            confidence=result.get("confidence")
        )
        db.add(extracted_req)
        
        # Save evidence
        for evidence_data in result.get("evidence", []):
            evidence = Evidence(
                run_id=run.id,
                field_path=evidence_data["field_path"],
                segment_idx=evidence_data.get("segment_idx"),
                snippet=evidence_data["snippet"],
                start_char=evidence_data.get("start_char"),
                end_char=evidence_data.get("end_char")
            )
            db.add(evidence)
        
        run.status = ExtractionStatus.COMPLETED
        run.finished_at = datetime.utcnow()
        run.model = llm_service.model_name
        db.commit()
        
    except Exception as e:
        if run:
            run.status = ExtractionStatus.FAILED
            db.commit()
        raise
    finally:
        db.close()

