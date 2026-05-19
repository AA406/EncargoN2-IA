from __future__ import annotations

from dataclasses import dataclass
from typing import List, Dict

from .config import CONFIDENCE_HIGH, CONFIDENCE_MEDIUM


@dataclass
class DecisionResult:
    action: str
    reason: str
    confidence: float
    requires_ticket: bool
    requires_human: bool


CATEGORY_KEYWORDS = {
    "acceso_cuenta": ["contraseña", "clave", "login", "ingresar", "cuenta", "bloqueada", "acceso"],
    "conectividad": ["vpn", "internet", "red", "wifi", "conexión", "conexion", "remoto"],
    "software": ["sistema", "aplicación", "aplicacion", "error", "pantalla", "software"],
    "hardware": ["equipo", "notebook", "pc", "impresora", "monitor", "teclado", "mouse"],
    "seguridad": ["phishing", "correo sospechoso", "virus", "malware", "hack", "seguridad"],
    "rrhh": ["vacaciones", "permiso", "licencia", "contrato", "rrhh", "recursos humanos"],
}

CRITICAL_KEYWORDS = [
    "caído", "caida", "no funciona nadie", "nadie puede", "facturar", "producción",
    "produccion", "urgente", "crítico", "critico", "bloqueo total", "seguridad", "phishing"
]

HIGH_KEYWORDS = ["no puedo trabajar", "bloqueado", "cliente", "ventas", "facturación", "facturacion"]


def normalize(text: str) -> str:
    return text.lower().strip()


def classify_request(text: str) -> str:
    normalized = normalize(text)
    scores = {}
    for category, keywords in CATEGORY_KEYWORDS.items():
        scores[category] = sum(1 for word in keywords if word in normalized)
    best_category, best_score = max(scores.items(), key=lambda item: item[1])
    return best_category if best_score > 0 else "general"


def evaluate_priority(text: str) -> str:
    normalized = normalize(text)
    if any(word in normalized for word in CRITICAL_KEYWORDS):
        return "critica"
    if any(word in normalized for word in HIGH_KEYWORDS):
        return "alta"
    return "normal"


def estimate_retrieval_confidence(results: List[Dict]) -> float:
    if not results:
        return 0.0
    best_score = max(float(item.get("score", 0.0)) for item in results)
    return round(min(max(best_score, 0.0), 1.0), 3)


def decide_action(text: str, retrieved_context: List[Dict]) -> DecisionResult:
    priority = evaluate_priority(text)
    confidence = estimate_retrieval_confidence(retrieved_context)

    if priority == "critica":
        return DecisionResult(
            action="crear_ticket_y_derivar",
            reason="La solicitud contiene señales de impacto crítico o interrupción operativa.",
            confidence=confidence,
            requires_ticket=True,
            requires_human=True,
        )

    if confidence >= CONFIDENCE_HIGH:
        return DecisionResult(
            action="responder_con_contexto",
            reason="La base de conocimiento recuperó información suficiente para responder.",
            confidence=confidence,
            requires_ticket=False,
            requires_human=False,
        )

    if confidence >= CONFIDENCE_MEDIUM:
        return DecisionResult(
            action="responder_y_crear_ticket",
            reason="Existe contexto parcial, pero se requiere seguimiento para asegurar continuidad.",
            confidence=confidence,
            requires_ticket=True,
            requires_human=False,
        )

    return DecisionResult(
        action="crear_ticket_y_derivar",
        reason="La recuperación semántica no encontró evidencia suficiente para una respuesta confiable.",
        confidence=confidence,
        requires_ticket=True,
        requires_human=True,
    )
