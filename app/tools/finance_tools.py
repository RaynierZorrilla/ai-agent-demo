def calculate_savings(income: float, expenses: float):
    return income - expenses

def determine_risk_level(income: float, expenses: float, debt: float):
    savings = income - expenses

    if debt > income * 2:
        return "high"
    elif savings < 500:
        return "medium"
        
    return "low"