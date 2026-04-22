import json
import os
import logging


import cohere
from dotenv import load_dotenv

from app.schemas import FinancialInput

load_dotenv()

co = cohere.ClientV2(api_key=os.getenv("COHERE_API_KEY"))

logging.basicConfig(level=logging.INFO)



def analyze_financial_data(data: FinancialInput) -> dict:
    logging.info(f"Input data: income={data.income}, expenses={data.expenses}, debt={data.debt}")
    response = co.chat(
        model="command-r-08-2024",
        messages=[
            {
                "role": "system",
                "content": (
                    "You are a financial risk assistant. "
                    "Return only valid JSON with the keys: "
                    "risk_level, summary, recommendation."
                ),
            },
            {
                "role": "user",
                "content": (
                    f"Analyze this financial profile:\n"
                    f"- Monthly income: {data.income}\n"
                    f"- Monthly expenses: {data.expenses}\n"
                    f"- Current debt: {data.debt}\n\n"
                    "Return ONLY valid JSON in this format:\n"
                    "{\n"
                    '  "risk_level": "low | medium | high",\n'
                    '  "summary": "short summary",\n'
                    '  "recommendation": "clear recommendation"\n'
                    "}"
                ),
            },
        ],
    )

    text_output = response.message.content[0].text.strip()

    try:
        return json.loads(text_output)
    except json.JSONDecodeError:
        return {
            "risk_level": "unknown",
            "summary": "Could not parse model response cleanly.",
            "recommendation": text_output,
        }