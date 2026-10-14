from __future__ import annotations
import uuid
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from backend.llm import get_llm
from backend.models import EvalCase, EvalRun
from backend.utils.text import token_set

def score_faithfulness(answer: str, context: str) -> float:
    a, c = token_set(answer), token_set(context)
    if not a: return 0.0
    return round(len(a & c) / len(a), 3)

def score_relevance(answer: str, question: str) -> float:
    a, q = token_set(answer), token_set(question)
    if not q: return 0.0
    return round(len(a & q) / len(q), 3)

async def add_case(session: AsyncSession, question: str, context: str, gold: str = "") -> EvalCase:
    row = EvalCase(id=uuid.uuid4().hex[:10], question=question.strip(), context=context.strip(), gold=gold.strip())
    session.add(row); await session.commit(); await session.refresh(row); return row

async def list_cases(session: AsyncSession) -> list[EvalCase]:
    return list((await session.execute(select(EvalCase))).scalars())

async def run_case(session: AsyncSession, case_id: str) -> EvalRun:
    case = await session.get(EvalCase, case_id)
    if not case: raise ValueError("not found")
    llm = get_llm()
    answer = await llm.complete(f"Context:\n{case.context}\n\nQ: {case.question}", system="Answer only from context.")
    run = EvalRun(id=uuid.uuid4().hex[:10], case_id=case_id, answer=answer,
                  faithfulness=score_faithfulness(answer, case.context),
                  relevance=score_relevance(answer, case.question))
    session.add(run); await session.commit(); await session.refresh(run); return run

async def list_runs(session: AsyncSession) -> list[EvalRun]:
    return list((await session.execute(select(EvalRun).order_by(EvalRun.created_at.desc()).limit(50))).scalars())
