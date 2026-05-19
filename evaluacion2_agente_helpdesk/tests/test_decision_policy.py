from src.decision_policy import classify_request, evaluate_priority, decide_action


def test_classify_password_request():
    assert classify_request("Olvidé mi contraseña") == "acceso_cuenta"


def test_critical_sales_system_request():
    assert evaluate_priority("El sistema de ventas está caído y nadie puede facturar") == "critica"


def test_low_confidence_creates_escalation():
    decision = decide_action("error desconocido sin manual", [])
    assert decision.requires_ticket is True
    assert decision.requires_human is True
