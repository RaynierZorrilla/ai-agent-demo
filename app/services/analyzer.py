import json
import os
import logging


import cohere
from dotenv import load_dotenv

from app.schemas import FinancialInput
from app.memory.store import save_interaction, get_recent_interactions
from app.tools.finance_tools import calculate_savings, determine_risk_level

load_dotenv()
co = cohere.ClientV2(api_key=os.getenv("COHERE_API_KEY"))

logging.basicConfig(level=logging.INFO)

TOOLS =  {
    "calculate_savings": calculate_savings, 
    "determine_risk_level": determine_risk_level}



def analyze_financial_data(data: FinancialInput) -> dict:
    logging.info("Starting analysis with memory...")

    recent_memory = []
    if data.user_id:
        recent_memory = get_recent_interactions(data.user_id)

    

    #Decide the tools to use
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
                    "Decide which tools should be used\n"
                    "Return only valid JSON.\n"
                ),
            },
            {
                "role": "user",
                "content": (
                    f"Recent memory:\n{json.dumps(recent_memory, indent=2)}\n\n"
                    f"Current Input:\n"
                    f"income: {data.income}\n"
                    f"expenses: {data.expenses}\n"
                    f"debt: {data.debt}\n\n"
                    "Return JSON like: \n"
                    "{\n"
                    '  "tools": [tools_name]\n'
                    "}"
                ),
            },
        ],
    )

    raw = response.message.content[0].text.strip()

    logging.info(f"Tool decision response: {raw}")

    if raw.startswith("```"):
        raw = raw.replace("```json", "").replace("```", "").strip()

    parsed = json.loads(raw)

    selected_tools = parsed.get("tools", [])

    results = {}

    # Execute tools
    for tool_name in selected_tools:

        if tool_name not in TOOLS:
            continue

        tool_function = TOOLS[tool_name]

        if tool_name == "calculate_savings":
            results[tool_name] = tool_function(
                data.income,
                data.expenses,
            )

        elif tool_name == "detect_risk_level":
            results[tool_name] = tool_function(
                data.income,
                data.expenses,
                data.debt,
            )

    # Generate final response
    final_response = co.chat(
        model="command-r-08-2024",
        messages=[
            {
                "role": "system",
                "content": ( "You are a financial divisor.\n"
                "Use the tools results to generate a advice.\n"
                "Return only valid JSON.\n"
                ),
            },
            {
                "role": "user",
                "content": (
                    f"Recent memory:\n{json.dumps(recent_memory, indent=2)}\n\n"
                    f"Tools results: {json.dumps(results, indent=2)}\n\n"
                    "Return JSON:\n"
                    "{\n"
                    '  "risk_level": "...", \n'
                    '  "summary": "...", \n'
                    '  "recommendation": "...", \n'
                    "}"
                ),
            },
        ],
    )

    output = final_response.message.content[0].text.strip()

    if output.startswith("```"):
        output = output.replace("```json", "").replace("```", "").strip()

    logging.info(f"Final output: {output}")

    return json.loads(output)

    #Save the interaction
    if data.user_id:
        save_interaction(
            data.user_id, 
            {
                "input": {
                    "income": data.income,
                    "expenses": data.expenses,
                    "debt": data.debt,
                },
                "tools": selected_tools,
                "tool_results": results,
                "final_response": output,
        })

    return json.loads(output)