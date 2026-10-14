from fastapi import APIRouter, Depends, Form, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.ext.asyncio import AsyncSession
from backend.db import get_db
from backend.services import rag_eval as svc

router = APIRouter()
templates = Jinja2Templates(directory="backend/templates")

@router.get("/", response_class=HTMLResponse)
async def home(request: Request, db: AsyncSession = Depends(get_db)):
    return templates.TemplateResponse("index.html", {"request": request, "title": "RAG Eval Dashboard",
        "cases": await svc.list_cases(db), "runs": await svc.list_runs(db)})

@router.post("/ui/cases")
async def ui_c(question: str = Form(...), context: str = Form(...), gold: str = Form(""), db: AsyncSession = Depends(get_db)):
    await svc.add_case(db, question, context, gold); return RedirectResponse("/", status_code=303)

@router.post("/ui/run")
async def ui_r(case_id: str = Form(...), db: AsyncSession = Depends(get_db)):
    await svc.run_case(db, case_id); return RedirectResponse("/", status_code=303)
