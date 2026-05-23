from __future__ import annotations

import hashlib
import json
import math
import re
from datetime import UTC, datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
MEMORY_ROOT = ROOT / "memory"
VECTOR_SIZE = 128


def tokenize(text: str) -> list[str]:
    return re.findall(r"\b[a-zA-Z][a-zA-Z0-9_-]*\b", text.lower())


def stable_vector(text: str) -> list[float]:
    vector = [0.0] * VECTOR_SIZE

    for token in tokenize(text):
        digest = hashlib.sha256(token.encode("utf-8")).digest()
        index = int.from_bytes(digest[:2], "big") % VECTOR_SIZE
        sign = 1.0 if digest[2] % 2 == 0 else -1.0
        vector[index] += sign

    magnitude = math.sqrt(sum(value * value for value in vector))
    if magnitude == 0:
        return vector

    return [value / magnitude for value in vector]


def cosine(left: list[float], right: list[float]) -> float:
    if not left or not right:
        return 0.0
    return sum(a * b for a, b in zip(left, right))


def project_memory_path(project_id: str) -> Path:
    safe_project = project_id.replace("/", "-").replace("\\", "-")
    return MEMORY_ROOT / safe_project / "semantic-memory.json"


def load_memory(project_id: str) -> dict:
    path = project_memory_path(project_id)
    if not path.exists():
        return {"project_id": project_id, "items": []}
    return json.loads(path.read_text(encoding="utf-8"))


def save_memory(project_id: str, memory: dict) -> None:
    path = project_memory_path(project_id)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(memory, indent=2) + "\n", encoding="utf-8")


def upsert_memory(project_id: str, source_path: str, content: str, memory_type: str = "artifact") -> dict:
    memory = load_memory(project_id)
    item_id = hashlib.sha256(f"{project_id}:{source_path}:{memory_type}".encode("utf-8")).hexdigest()[:16]
    vector = stable_vector(content)

    item = {
        "item_id": item_id,
        "project_id": project_id,
        "source_path": source_path,
        "memory_type": memory_type,
        "content_preview": content[:500],
        "vector": vector,
        "updated_at": datetime.now(UTC).isoformat(),
    }

    memory["items"] = [existing for existing in memory.get("items", []) if existing["item_id"] != item_id]
    memory["items"].append(item)
    save_memory(project_id, memory)
    return item


def search_memory(project_id: str, query: str, top_k: int = 5) -> list[dict]:
    memory = load_memory(project_id)
    query_vector = stable_vector(query)
    results = []

    for item in memory.get("items", []):
        score = cosine(query_vector, item.get("vector", []))
        results.append({
            "score": round(score, 4),
            "item_id": item["item_id"],
            "source_path": item["source_path"],
            "memory_type": item["memory_type"],
            "content_preview": item.get("content_preview", ""),
        })

    return sorted(results, key=lambda result: result["score"], reverse=True)[:top_k]
