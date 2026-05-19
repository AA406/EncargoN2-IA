from __future__ import annotations

import json
from typing import Dict, List, Optional, TypedDict, Any

from langgraph.graph import StateGraph, END

from .config import AGENT_NAME, DEFAULT_USER_ID
from .decision_policy import classify_request, evaluate_priority, decide_action
from .memory import ConversationMemory, LongTermCaseMemory
from .planner import build_task_plan
from .semantic_retriever import SemanticRetriever
from .ticket_writer import create_ticket


class AgentState(TypedDict, total=False):
    user_id: str
    user_input: str
    history: List[Dict[str, Any]]
    category: str
    priority: str
    retrieved_context: List[Dict[str, Any]]
    decision: Dict[str, Any]
    plan: List[Dict[str, str]]
    response: str
    ticket: Optional[Dict[str, Any]]
    human_escalation: Optional[str]


class HelpdeskAgent:
    """Agente funcional con herramientas, memoria, recuperación y planificación."""

    def __init__(self):
        self.retriever = SemanticRetriever()
        self.short_memory = ConversationMemory()
        self.long_memory = LongTermCaseMemory()
        self.graph = self._build_graph()

    def _load_memory(self, state: AgentState) -> AgentState:
        user_id = state.get("user_id", DEFAULT_USER_ID)
        history = self.short_memory.load_recent(user_id, limit=8)
        state["history"] = history
        return state

    def _classify_and_retrieve(self, state: AgentState) -> AgentState:
        user_input = state["user_input"]
        state["category"] = classify_request(user_input)
        state["priority"] = evaluate_priority(user_input)
        state["retrieved_context"] = self.retriever.search(user_input, top_k=4)
        return state

    def _decide(self, state: AgentState) -> AgentState:
        decision = decide_action(state["user_input"], state.get("retrieved_context", []))
        state["decision"] = decision.__dict__
        state["plan"] = build_task_plan(state)
        return state

    def _act(self, state: AgentState) -> AgentState:
        action = state["decision"]["action"]
        user_id = state.get("user_id", DEFAULT_USER_ID)
        category = state.get("category", "general")
        priority = state.get("priority", "normal")
        reason = state["decision"]["reason"]
        context = state.get("retrieved_context", [])

        if action == "responder_con_contexto":
            state["response"] = self._build_contextual_answer(state)
            state["ticket"] = None
            state["human_escalation"] = None
            return state

        if action == "responder_y_crear_ticket":
            state["response"] = self._build_contextual_answer(state, caution=True)
            state["ticket"] = create_ticket(
                user_id=user_id,
                title="Seguimiento recomendado por confianza media",
                description=state["user_input"],
                category=category,
                priority=priority,
                reason=reason,
                metadata={"confidence": state["decision"].get("confidence"), "context": context[:2]},
            )
            state["human_escalation"] = None
            return state

        state["ticket"] = create_ticket(
            user_id=user_id,
            title="Derivación requerida por el agente",
            description=state["user_input"],
            category=category,
            priority=priority,
            reason=reason,
            metadata={"confidence": state["decision"].get("confidence"), "context": context[:2]},
        )
        state["human_escalation"] = "Caso derivado a soporte humano por criticidad o baja confianza."
        state["response"] = self._build_escalation_answer(state)
        return state

    def _persist_memory(self, state: AgentState) -> AgentState:
        user_id = state.get("user_id", DEFAULT_USER_ID)
        self.short_memory.append(user_id, "user", state["user_input"])
        self.short_memory.append(
            user_id,
            "agent",
            state.get("response", ""),
            metadata={
                "category": state.get("category"),
                "priority": state.get("priority"),
                "decision": state.get("decision"),
                "ticket_id": (state.get("ticket") or {}).get("ticket_id"),
            },
        )
        self.long_memory.save_case({
            "user_id": user_id,
            "input": state["user_input"],
            "category": state.get("category"),
            "priority": state.get("priority"),
            "decision": state.get("decision"),
            "ticket": state.get("ticket"),
            "response": state.get("response"),
        })
        return state

    def _build_graph(self):
        graph = StateGraph(AgentState)
        graph.add_node("load_memory", self._load_memory)
        graph.add_node("classify_and_retrieve", self._classify_and_retrieve)
        graph.add_node("decide", self._decide)
        graph.add_node("act", self._act)
        graph.add_node("persist_memory", self._persist_memory)

        graph.set_entry_point("load_memory")
        graph.add_edge("load_memory", "classify_and_retrieve")
        graph.add_edge("classify_and_retrieve", "decide")
        graph.add_edge("decide", "act")
        graph.add_edge("act", "persist_memory")
        graph.add_edge("persist_memory", END)
        return graph.compile()

    def _build_contextual_answer(self, state: AgentState, caution: bool = False) -> str:
        context = state.get("retrieved_context", [])
        sources = ", ".join(sorted({item.get("source", "base") for item in context[:3]})) or "base de conocimiento"
        best = context[0]["text"] if context else "No se encontró un procedimiento específico."
        prefix = "Encontré información parcial y dejaré seguimiento. " if caution else "Encontré un procedimiento relacionado. "
        return (
            f"{prefix}\n"
            f"Categoría detectada: {state.get('category')} | Prioridad: {state.get('priority')} | "
            f"Confianza: {state.get('decision', {}).get('confidence')}\n\n"
            f"Respuesta sugerida:\n{best}\n\n"
            f"Fuentes consultadas: {sources}."
        )

    def _build_escalation_answer(self, state: AgentState) -> str:
        ticket = state.get("ticket") or {}
        return (
            "No es recomendable cerrar este caso solo con respuesta automática.\n"
            f"Motivo: {state.get('decision', {}).get('reason')}\n"
            f"Categoría: {state.get('category')} | Prioridad: {state.get('priority')} | "
            f"Confianza: {state.get('decision', {}).get('confidence')}\n"
            f"Ticket generado: {ticket.get('ticket_id', 'sin ticket')}\n"
            "Acción: derivación a soporte humano para revisión y seguimiento."
        )

    def run(self, user_input: str, user_id: str = DEFAULT_USER_ID) -> AgentState:
        initial_state: AgentState = {"user_id": user_id, "user_input": user_input}
        return self.graph.invoke(initial_state)

    def print_result(self, state: AgentState) -> None:
        print(f"\n=== {AGENT_NAME} ===")
        print(state.get("response", "Sin respuesta"))
        print("\n--- Plan ejecutado ---")
        for step in state.get("plan", []):
            print(f"{step['step']}. {step['task']}: {step['purpose']}")
        if state.get("ticket"):
            print("\n--- Ticket ---")
            print(json.dumps(state["ticket"], ensure_ascii=False, indent=2))
