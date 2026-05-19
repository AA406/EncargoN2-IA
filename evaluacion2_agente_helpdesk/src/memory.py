from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List, Any

from .config import MEMORY_DIR


class ConversationMemory:
    """Memoria de corto plazo persistente por usuario.

    Guarda mensajes en JSONL para permitir continuidad en conversaciones largas.
    """

    def __init__(self, memory_dir: Path = MEMORY_DIR):
        self.memory_dir = Path(memory_dir)
        self.memory_dir.mkdir(parents=True, exist_ok=True)

    def _path(self, user_id: str) -> Path:
        safe_user = user_id.replace("/", "_").replace("\\", "_")
        return self.memory_dir / f"conversation_{safe_user}.jsonl"

    def append(self, user_id: str, role: str, content: str, metadata: Dict[str, Any] | None = None) -> None:
        event = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "user_id": user_id,
            "role": role,
            "content": content,
            "metadata": metadata or {},
        }
        with open(self._path(user_id), "a", encoding="utf-8") as file:
            file.write(json.dumps(event, ensure_ascii=False) + "\n")

    def load_recent(self, user_id: str, limit: int = 8) -> List[Dict[str, Any]]:
        path = self._path(user_id)
        if not path.exists():
            return []
        lines = path.read_text(encoding="utf-8").splitlines()
        events = [json.loads(line) for line in lines if line.strip()]
        return events[-limit:]


class LongTermCaseMemory:
    """Memoria de largo plazo para registrar casos y decisiones tomadas."""

    def __init__(self, memory_dir: Path = MEMORY_DIR):
        self.path = Path(memory_dir) / "long_term_cases.jsonl"
        self.path.parent.mkdir(parents=True, exist_ok=True)

    def save_case(self, case: Dict[str, Any]) -> None:
        case = dict(case)
        case.setdefault("saved_at", datetime.now(timezone.utc).isoformat())
        with open(self.path, "a", encoding="utf-8") as file:
            file.write(json.dumps(case, ensure_ascii=False) + "\n")

    def load_cases(self, limit: int = 20) -> List[Dict[str, Any]]:
        if not self.path.exists():
            return []
        lines = self.path.read_text(encoding="utf-8").splitlines()
        cases = [json.loads(line) for line in lines if line.strip()]
        return cases[-limit:]

    def search_by_keyword(self, query: str, limit: int = 5) -> List[Dict[str, Any]]:
        terms = set(query.lower().split())
        scored = []
        for case in self.load_cases(limit=100):
            text = json.dumps(case, ensure_ascii=False).lower()
            score = sum(1 for term in terms if term in text)
            if score > 0:
                scored.append((score, case))
        scored.sort(key=lambda item: item[0], reverse=True)
        return [case for _, case in scored[:limit]]
