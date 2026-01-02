from sqlalchemy.orm import Session
from app.models.case import Case
from app.schemas.case import CaseCreate, CaseUpdate

class CaseService:
    def __init__(self, db: Session):
        self.db = db
    
    def create_case(self, case_data: CaseCreate) -> Case:
        case = Case(**case_data.dict())
        self.db.add(case)
        self.db.commit()
        self.db.refresh(case)
        return case
    
    def get_case(self, case_id: int) -> Case:
        return self.db.query(Case).filter(Case.id == case_id).first()
    
    def list_cases(self, skip: int = 0, limit: int = 100):
        return self.db.query(Case).offset(skip).limit(limit).all()
    
    def update_case(self, case_id: int, case_data: CaseUpdate) -> Case:
        case = self.get_case(case_id)
        if not case:
            return None
        
        update_data = case_data.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(case, field, value)
        
        self.db.commit()
        self.db.refresh(case)
        return case

