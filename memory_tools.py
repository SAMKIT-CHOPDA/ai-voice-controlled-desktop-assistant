import json
from pathlib import Path


# =============================================================
# MEMORY FILE
# =============================================================

MEMORY_FILE = Path.home() / "Documents" / "AI Assistant Memory" / "memory.json"


# =============================================================
# LOAD MEMORY
# =============================================================

def _load_memory():
    """
    Load all saved memories from the JSON file.
    """

    if not MEMORY_FILE.exists():
        return []

    try:
        with open(MEMORY_FILE, "r", encoding="utf-8") as file:
            data = json.load(file)

        if isinstance(data, list):
            return data

        return []

    except (json.JSONDecodeError, OSError):
        return []


# =============================================================
# SAVE MEMORY FILE
# =============================================================

def _save_memory(memories):
    """
    Save memories to the JSON file.
    """

    MEMORY_FILE.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    with open(
        MEMORY_FILE,
        "w",
        encoding="utf-8"
    ) as file:

        json.dump(
            memories,
            file,
            indent=4,
            ensure_ascii=False
        )


# =============================================================
# ADD MEMORY
# =============================================================

def save_memory(memory):
    """
    Save a new long-term memory.
    """

    memory = memory.strip()

    if not memory:
        return "I cannot save an empty memory."

    memories = _load_memory()

    # Avoid exact duplicates
    if memory.lower() in [
        item.lower()
        for item in memories
    ]:
        return "I already have that saved in memory."

    memories.append(memory)

    _save_memory(memories)

    return f"I'll remember that: {memory}"


# =============================================================
# SEARCH MEMORY
# =============================================================

def search_memory(query):
    """
    Search saved memories for relevant information.
    """

    query = query.lower().strip()

    if not query:
        return "Please provide something to search for."

    memories = _load_memory()

    if not memories:
        return "I don't have any saved memories yet."

    # Simple keyword matching
    query_words = set(query.split())

    matches = []

    for memory in memories:

        memory_words = set(
            memory.lower().split()
        )

        if query_words & memory_words:
            matches.append(memory)

    if not matches:
        return f"I couldn't find any memory related to '{query}'."

    output = [
        f"Found {len(matches)} relevant memory/memories:"
    ]

    for memory in matches:
        output.append(f"- {memory}")

    return "\n".join(output)


# =============================================================
# READ ALL MEMORIES
# =============================================================

def read_memories():
    """
    Return all saved memories.
    """

    memories = _load_memory()

    if not memories:
        return "I don't have any saved memories."

    output = [
        f"I have {len(memories)} saved memor{'y' if len(memories) == 1 else 'ies'}:"
    ]

    for memory in memories:
        output.append(f"- {memory}")

    return "\n".join(output)


# =============================================================
# DELETE MEMORY
# =============================================================

def delete_memory(memory):
    """
    Delete an exact saved memory.
    """

    memory = memory.strip()

    if not memory:
        return "Please specify which memory to delete."

    memories = _load_memory()

    for saved_memory in memories:

        if saved_memory.lower() == memory.lower():

            memories.remove(saved_memory)

            _save_memory(memories)

            return f"I forgot that memory: {saved_memory}"

    return "I couldn't find that exact memory."