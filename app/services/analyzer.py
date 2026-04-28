import json
import os
import logging

import cohere
from dotenv import load_dotenv

from app.schemas import FinancialInput
from app.memory.store import save_interaction, get_recent_interactions
from app.tools.finance_tools import calculate_savings, determine_risk_level
from app.knowledge.finance_knowledge import retrieve_relevant_knowledge

load_dotenv()

logging.basicConfig(level=logging.INFO)

co = cohere.ClientV2(api_key=os.getenv("COHERE_API_KEY"))

TOOLS = {
    "calculate_savings": calculate_savings,
    "determine_risk_level": determine_risk_level,
}


def clean_json_response(text: str) -> str:
    text = text.strip()

    if text.startswith("```"):
        text = text.replace("```json", "").replace("```", "").strip()

    return text


def analyze_financial_data(data: FinancialInput) -> dict:
    logging.info("Starting analysis with memory and retrieval...")

    recent_memory = []
    if data.user_id:
        recent_memory = get_recent_interactions(data.user_id)

    # 1. Decide tools
    response = co.chat(
        model="command-r-08-2024",
        messages=[
            {
                "role": "system",
                "content": (
                    "You are a financial AI agent.\n"
                    "Available tools:\n"
                    "- calculate_savings\n"
                    "- determine_risk_level\n\n"
                    "Decide which tools should be used.\n"
                    "Return ONLY valid JSON."
                ),
            },
            {
                "role": "user",
                "content": (
                    f"Recent memory:\n{json.dumps(recent_memory, indent=2)}\n\n"
                    f"Current input:\n"
                    f"Income: {data.income}\n"
                    f"Expenses: {data.expenses}\n"
                    f"Debt: {data.debt}\n\n"
                    "Return JSON exactly like this:\n"
                    "{\n"
                    '  "tools": ["calculate_savings", "determine_risk_level"]\n'
                    "}"
                ),
            },
        ],
    )

    raw = clean_json_response(response.message.content[0].text)
    logging.info(f"Tool decision response: {raw}")

    parsed = json.loads(raw)
    selected_tools = parsed.get("tools", [])

    results = {}

    # 2. Execute tools
    for tool_name in selected_tools:
        if tool_name not in TOOLS:
            continue

        tool_function = TOOLS[tool_name]

        if tool_name == "calculate_savings":
            results[tool_name] = tool_function(data.income, data.expenses)

        elif tool_name == "determine_risk_level":
            results[tool_name] = tool_function(
                data.income,
                data.expenses,
                data.debt,
            )

    # 3. Retrieve knowledge
    knowledge = retrieve_relevant_knowledge(
        data.income,
        data.expenses,
        data.debt,
    )

    logging.info(f"Retrieved knowledge: {knowledge}")

    # 4. Generate final response
    final_response = co.chat(
        model="command-r-08-2024",
        messages=[
            {
                "role": "system",
                "content": (
                    "You are a financial advisor.\n"
                    "Use recent memory, retrieved knowledge, and tool results to generate advice.\n"
                    "Return ONLY valid JSON with keys: risk_level, summary, recommendation."
                ),
            },
            {
                "role": "user",
                "content": (
                    f"Recent memory:\n{json.dumps(recent_memory, indent=2)}\n\n"
                    f"Retrieved knowledge:\n{json.dumps(knowledge, indent=2)}\n\n"
                    f"Current tool results:\n{json.dumps(results, indent=2)}\n\n"
                    "Return JSON:\n"
                    "{\n"
                    '  "risk_level": "...",\n'
                    '  "summary": "...",\n'
                    '  "recommendation": "..."\n'
                    "}"
                ),
            },
        ],
    )

    output = clean_json_response(final_response.message.content[0].text)
    logging.info(f"Final output: {output}")

    parsed_output = json.loads(output)

    # 5. Save interaction
    if data.user_id:
        save_interaction(
            data.user_id,
            {
                "input": {
                    "income": data.income,
                    "expenses": data.expenses,
                    "debt": data.debt,
                },
                "tools_used": selected_tools,
                "tool_results": results,
                "retrieved_knowledge": knowledge,
                "final_response": parsed_output,
            },
        )

    return parsed_output