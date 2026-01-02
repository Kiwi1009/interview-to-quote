from sqlalchemy.orm import Session
from typing import List, Optional, Dict, Any
from app.models.case import Case
from app.models.plan import Plan, PlanCode
from app.models.quote_item import QuoteItem
from app.models.extraction_run import ExtractionRun
from app.services.pricing_engine import PricingEngine
from app.schemas.plan import PlanUpdate

class PlanService:
    def __init__(self, db: Session):
        self.db = db
        self.pricing_engine = PricingEngine()
    
    def generate_plans(self, case_id: int, run_id: Optional[int] = None) -> Optional[List[Plan]]:
        case = self.db.query(Case).filter(Case.id == case_id).first()
        if not case:
            return None
        
        # Get requirements
        from app.services.extraction_service import ExtractionService
        extraction_service = ExtractionService(self.db)
        requirements = extraction_service.get_requirements(case_id, run_id)
        if not requirements:
            return None
        
        # Get or create run
        if run_id:
            run = self.db.query(ExtractionRun).filter(ExtractionRun.id == run_id).first()
        else:
            run = self.db.query(ExtractionRun).filter(
                ExtractionRun.case_id == case_id
            ).order_by(ExtractionRun.version.desc()).first()
        
        # Check if plans already exist
        existing_plans = self.db.query(Plan).filter(
            Plan.case_id == case_id,
            Plan.run_id == run.id if run else None
        ).all()
        if existing_plans:
            return existing_plans
        
        # Generate 3 plans
        plans = []
        for plan_code in [PlanCode.P1, PlanCode.P2, PlanCode.P3]:
            plan = self._create_plan(case_id, run.id if run else None, plan_code, requirements.jsonb_data)
            plans.append(plan)
        
        return plans
    
    def _create_plan(self, case_id: int, run_id: Optional[int], plan_code: PlanCode, requirements: Dict[str, Any]) -> Plan:
        # Generate plan based on code
        plan_spec = self.pricing_engine.generate_plan_spec(plan_code, requirements)
        
        plan = Plan(
            case_id=case_id,
            run_id=run_id,
            plan_code=plan_code,
            name=plan_spec["name"],
            assumptions_jsonb=plan_spec["assumptions"]
        )
        self.db.add(plan)
        self.db.flush()
        
        # Generate quote items
        quote_items = self.pricing_engine.generate_quote_items(plan_code, requirements)
        for item_data in quote_items:
            item = QuoteItem(
                plan_id=plan.id,
                **item_data
            )
            self.db.add(item)
        
        self.db.commit()
        self.db.refresh(plan)
        return plan
    
    def list_plans(self, case_id: int, run_id: Optional[int] = None) -> List[Plan]:
        query = self.db.query(Plan).filter(Plan.case_id == case_id)
        if run_id:
            query = query.filter(Plan.run_id == run_id)
        return query.all()
    
    def update_plan(self, plan_id: int, plan_data: PlanUpdate) -> Optional[Plan]:
        plan = self.db.query(Plan).filter(Plan.id == plan_id).first()
        if not plan:
            return None
        
        if plan_data.assumptions_jsonb is not None:
            plan.assumptions_jsonb = plan_data.assumptions_jsonb
        
        self.db.commit()
        self.db.refresh(plan)
        return plan

