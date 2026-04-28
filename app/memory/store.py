from typing import Any

MEMORY_STORE: dict[str, list[dict[str, Any]]] = {}

def save_interaction(user_id: str, interaction: dict[str, Any]) -> None:
    if user_id not in MEMORY_STORE:
        MEMORY_STORE[user_id] = []

    MEMORY_STORE[user_id].append(interaction)

    #keep only the last 3 interactions
    MEMORY_STORE[user_id] = MEMORY_STORE[user_id][-3:]

def get_recent_interactions(user_id: str) -> list[dict[str, Any]]:
    return MEMORY_STORE.get(user_id, [])