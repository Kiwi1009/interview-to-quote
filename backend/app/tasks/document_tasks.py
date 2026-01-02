from app.celery_app import celery_app
from app.core.database import SessionLocal
from app.models.case import Case
from app.models.document import Document, DocumentType, DocumentFormat
from app.models.extraction_run import ExtractionRun
from app.services.document_generator import DocumentGenerator
from typing import List

@celery_app.task
def generate_documents_task(case_id: int, run_id: int, doc_types: List[str], doc_formats: List[str]):
    """Async task to generate documents"""
    db = SessionLocal()
    try:
        case = db.query(Case).filter(Case.id == case_id).first()
        if not case:
            return
        
        run = None
        if run_id:
            run = db.query(ExtractionRun).filter(ExtractionRun.id == run_id).first()
        
        generator = DocumentGenerator(db)
        documents = []
        
        for doc_type_str in doc_types:
            doc_type = DocumentType(doc_type_str)
            for format_str in doc_formats:
                format_enum = DocumentFormat(format_str)
                doc_path = generator.generate_document(case_id, run_id, doc_type, format_enum)
                
                if doc_path:
                    doc = Document(
                        case_id=case_id,
                        run_id=run_id,
                        doc_type=doc_type,
                        format=format_enum,
                        path=doc_path
                    )
                    db.add(doc)
                    documents.append(doc)
        
        db.commit()
        return [d.id for d in documents]
        
    except Exception as e:
        db.rollback()
        raise
    finally:
        db.close()

