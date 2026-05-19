from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from uuid import uuid4
from typing import Optional, Dict, Any

from .config import TICKET_FILE


def create_ticket(
    user_id: str,
    title: str,
    description: str,
    category: str,
    priority: str,
    reason: str,
    metadata: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    ticket = {
        "ticket_id": f"TK-{uuid4().hex[:8].upper()}",
        "created_at": datetime.now(timezone.utc).isoformat(),
        "user_id": user_id,
        "title": title,
        "description": description,
        "category": category,
        "priority": priority,
        "reason": reason,
        "status": "abierto",
        "metadata": metadata or {},
    }

    Path(TICKET_FILE).parent.mkdir(parents=True, exist_ok=True)
    with open(TICKET_FILE, "a", encoding="utf-8") as file:
        file.write(json.dumps(ticket, ensure_ascii=False) + "\n")
    return ticket


def list_tickets(limit: int = 20):
    if not Path(TICKET_FILE).exists():
        return []
    lines = Path(TICKET_FILE).read_text(encoding="utf-8").splitlines()
    tickets = [json.loads(line) for line in lines if line.strip()]
    return tickets[-limit:]
