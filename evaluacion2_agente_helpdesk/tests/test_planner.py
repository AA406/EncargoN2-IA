from src.planner import build_task_plan


def test_planner_adds_ticket_for_critical_action():
    plan = build_task_plan({
        "priority": "critica",
        "decision": {"action": "crear_ticket_y_derivar"},
    })
    tasks = [item["task"] for item in plan]
    assert "Crear ticket" in tasks
    assert "Derivar a soporte humano" in tasks
