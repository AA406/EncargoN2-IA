from __future__ import annotations

from typing import Dict, List


def build_task_plan(state: Dict) -> List[Dict[str, str]]:
    """Genera una secuencia de tareas para el agente según prioridad y contexto."""
    priority = state.get("priority", "normal")
    decision = state.get("decision", {})
    action = decision.get("action", "responder_con_contexto") if isinstance(decision, dict) else str(decision)

    base_plan = [
        {"step": "1", "task": "Cargar memoria reciente", "purpose": "Mantener continuidad de la conversación."},
        {"step": "2", "task": "Clasificar solicitud", "purpose": "Identificar categoría y prioridad inicial."},
        {"step": "3", "task": "Recuperar contexto semántico", "purpose": "Buscar evidencia en la base de conocimiento."},
        {"step": "4", "task": "Evaluar confianza", "purpose": "Determinar si la respuesta automática es suficiente."},
    ]

    if priority == "critica" or action == "crear_ticket_y_derivar":
        base_plan.extend([
            {"step": "5", "task": "Crear ticket", "purpose": "Registrar el incidente para seguimiento."},
            {"step": "6", "task": "Derivar a soporte humano", "purpose": "Reducir riesgo operativo en casos críticos o ambiguos."},
        ])
    elif action == "responder_y_crear_ticket":
        base_plan.extend([
            {"step": "5", "task": "Responder con advertencia", "purpose": "Entregar orientación con trazabilidad limitada."},
            {"step": "6", "task": "Crear ticket preventivo", "purpose": "Asegurar seguimiento posterior."},
        ])
    else:
        base_plan.append(
            {"step": "5", "task": "Responder con contexto", "purpose": "Resolver la consulta sin escalar."}
        )

    base_plan.append({"step": "final", "task": "Guardar memoria", "purpose": "Registrar acción y resultado del caso."})
    return base_plan
