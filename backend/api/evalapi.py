from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field
from sqlalchemy.ext.asyncio import AsyncSession
from backend.db import get_db
from backend.services import rag_eval as svc

class CaseIn(BaseModel):
    question: str = Field(min_length=3)
    context: str = Field(min_length=5)
    gold: str = ""

router = APIRouter()

@router.get("/cases")
async def cases(db: AsyncSession = Depends(get_db)):
    rows = await svc.list_cases(db)
    return {"cases": [{"id": c.id, "question": c.question} for c in rows]}

@router.post("/cases")
async def add(payload: CaseIn, db: AsyncSession = Depends(get_db)):
    c = await svc.add_case(db, payload.question, payload.context, payload.gold); return {"id": c.id}

@router.post("/cases/{case_id}/run")
async def run(case_id: str, db: AsyncSession = Depends(get_db)):
    try:
        r = await svc.run_case(db, case_id)
    except ValueError as exc:
        raise HTTPException(404, str(exc)) from exc
    return {"id": r.id, "faithfulness": r.faithfulness, "relevance": r.relevance, "answer": r.answer[:400]}

@router.get("/runs")
async def runs(db: AsyncSession = Depends(get_db)):
    rows = await svc.list_runs(db)
    return {"runs": [{"id": r.id, "case_id": r.case_id, "faithfulness": r.faithfulness, "relevance": r.relevance} for r in rows]}
