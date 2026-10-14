# Dev server for rag-eval-dashboard
$env:LLM_MODE = "mock"
uvicorn backend.main:app --reload --port 8000
