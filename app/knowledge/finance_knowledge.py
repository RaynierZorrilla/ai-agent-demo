KNOWLEDGE_BASE = [
    {
        "topic": "high_debt",
        "content": (
            "High debt compared to income may indicate financial instability. "
            "Reducing debt and increasing emergency savings is recommended."
        ),
    },
    {
        "topic": "low_savings",
        "content": (
            "Low monthly savings can increase financial vulnerability. "
            "Users should reduce discretionary expenses when possible."
        ),
    },
    {
        "topic": "healthy_finances",
        "content": (
            "Positive cash flow and controlled debt levels are indicators "
            "of healthy financial behavior."
        ),
    },
]

def retrieve_relevant_knowledge(
    income: float,
    expenses: float,
    debt: float,
) -> list[str]:

    relevant = []

    savings = income - expenses

    if debt > income * 2:
        relevant.append(KNOWLEDGE_BASE[0]["content"])

    if savings < 500:
        relevant.append(KNOWLEDGE_BASE[1]["content"])

    if savings >= 1000 and debt < income:
        relevant.append(KNOWLEDGE_BASE[2]["content"])

    return relevant