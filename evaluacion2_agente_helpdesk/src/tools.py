from __future__ import annotations

import json
from typing import Dict

from langchain_core.tools import tool

from .decision_policy import classify_request, evaluate_priority
from .semantic_retriever import SemanticRetriever
from .ticket_writer import create_ticket

_retriever = SemanticRetriever()


def query_knowledge_base(query: str) -> str:
    results = _retriever.search(query, top_k=4)
    return json.dumps(results, ensure_ascii=False, indent=2)


def priority_tool_text(query: str) -> str:
    return evaluate_priority(query)


def summarize_case_text(query: str) -> str:
    category = classify_request(query)
    priority = evaluate_priority(query)
    return f"Categoría: {category}. Prioridad: {priority}. Resumen: {query[:220]}"


def create_support_ticket(payload: Dict) -> str:
    ticket = create_ticket(
        user_id=payload.get("user_id", "usuario_demo"),
        title=payload.get("title", "Solicitud de soporte"),
        description=payload.get("description", "Sin descripción"),
        category=payload.get("category", "general"),
        priority=payload.get("priority", "normal"),
        reason=payload.get("reason", "Creado por política de decisión del agente."),
        metadata=payload.get("metadata", {}),
    )
    return json.dumps(ticket, ensure_ascii=False, indent=2)


def human_escalation_text(reason: str) -> str:
    return (
        "Derivación generada para soporte humano. "
        f"Motivo: {reason}. El agente mantendrá el caso registrado para seguimiento."
    )


@tool("consultar_base_conocimiento")
def consultar_base_conocimiento(query: str) -> str:
    """Consulta documentos internos mediante recuperación semántica."""
    return query_knowledge_base(query)


@tool("evaluar_prioridad")
def evaluar_prioridad_tool(query: str) -> str:
    """Evalúa la prioridad operacional de una solicitud de soporte."""
    return priority_tool_text(query)


@tool("resumir_caso")
def resumir_caso(query: str) -> str:
    """Resume una solicitud de soporte y entrega categoría/prioridad."""
    return summarize_case_text(query)


@tool("crear_ticket_soporte")
def crear_ticket_soporte(payload: Dict) -> str:
    """Crea un ticket de soporte en almacenamiento local JSONL."""
    return create_support_ticket(payload)


@tool("derivar_a_humano")
def derivar_a_humano(reason: str) -> str:
    """Genera un mensaje de derivación humana para casos críticos o ambiguos."""
    return human_escalation_text(reason)


AGENT_TOOLS = [
    consultar_base_conocimiento,
    evaluar_prioridad_tool,
    resumir_caso,
    crear_ticket_soporte,
    derivar_a_humano,
]
