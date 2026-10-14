from __future__ import annotations
from datetime import datetime
from sqlalchemy import DateTime, Float, String, Text
from sqlalchemy.orm import Mapped, mapped_column
from backend.db import Base
def utcnow(): return datetime.utcnow()
class EvalCase(Base):
    __tablename__ = "eval_cases"
    id: Mapped[str] = mapped_column(String(32), primary_key=True)
    question: Mapped[str] = mapped_column(Text)
    context: Mapped[str] = mapped_column(Text)
    gold: Mapped[str] = mapped_column(Text, default="")
class EvalRun(Base):
    __tablename__ = "eval_runs"
    id: Mapped[str] = mapped_column(String(32), primary_key=True)
    case_id: Mapped[str] = mapped_column(String(32), index=True)
    answer: Mapped[str] = mapped_column(Text)
    faithfulness: Mapped[float] = mapped_column(Float, default=0.0)
    relevance: Mapped[float] = mapped_column(Float, default=0.0)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=utcnow)
