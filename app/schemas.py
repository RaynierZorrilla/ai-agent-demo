from pydantic import BaseModel, Field

class FinancialInput(BaseModel):
    income: float = Field(..., gt=0, description="Monthly income")
    expenses: float = Field(..., gt=0, description="Monthly expenses")
    debt: float = Field(..., gt=0, description="Monthly debt payments")

class AnalysisResponse(BaseModel):
    risk_level: str
    summary: str
    recommendation: str