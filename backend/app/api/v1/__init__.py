from fastapi import APIRouter
from app.api.v1 import cases, uploads, extraction, plans, documents

api_router = APIRouter()

api_router.include_router(cases.router, prefix="/cases", tags=["cases"])
api_router.include_router(uploads.router, prefix="/cases", tags=["uploads"])
api_router.include_router(extraction.router, prefix="/cases", tags=["extraction"])
api_router.include_router(plans.router, prefix="/cases", tags=["plans"])
api_router.include_router(documents.router, prefix="/cases", tags=["documents"])

