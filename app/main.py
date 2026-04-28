from fastapi import FastAPI, HTTPException

from app.schemas import FinancialInput, AnalysisResponse
from app.services.analyzer import analyze_financial_data

app = FastAPI(
    title="Financial AI Agent API",
    description="AI agent prototype with tool calling, memory, and lightweight retrieval.",
    version="1.0.0",
)

@app.get("/")
async def root():
    return {"message": "AI Agent API is running"}

@app.get("/health")
def health_check():
    return {"status": "ok"}

@app.post("/analyze", response_model=AnalysisResponse)
def analyze(data: FinancialInput):
    try:
        result = analyze_financial_data(data)
        return result
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc))