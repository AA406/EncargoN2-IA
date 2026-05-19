from pathlib import Path
from datetime import datetime
from src.agent import HelpdeskAgent

EVIDENCE_DIR = Path("evidencias")
EVIDENCE_DIR.mkdir(exist_ok=True)

CASES = {
    "caso_1_consulta_resuelta.md": "Olvidé mi contraseña y no puedo ingresar al sistema.",
    "caso_2_creacion_ticket.md": "El sistema de ventas está caído y nadie puede facturar, es urgente.",
    "caso_3_escalamiento_humano.md": "Tengo un error raro que no aparece en ningún manual y necesito ayuda.",
    "caso_4_memoria_contextual.md": "Ayer tuve problemas con VPN y ahora necesito saber si quedó registro del caso.",
}

if __name__ == "__main__":
    agent = HelpdeskAgent()
    for filename, query in CASES.items():
        result = agent.run(query, user_id="evidencia_ep2")
        content = [
            f"# Evidencia - {filename.replace('_', ' ').replace('.md', '')}",
            "",
            f"Fecha de ejecución: {datetime.now().isoformat(timespec='seconds')}",
            "",
            "## Consulta",
            query,
            "",
            "## Respuesta del agente",
            result.get("response", ""),
            "",
            "## Decisión",
            str(result.get("decision")),
            "",
            "## Plan ejecutado",
        ]
        for step in result.get("plan", []):
            content.append(f"- {step['step']}. **{step['task']}**: {step['purpose']}")
        if result.get("ticket"):
            content.extend(["", "## Ticket generado", "```json", str(result.get("ticket")), "```"])
        (EVIDENCE_DIR / filename).write_text("\n".join(content), encoding="utf-8")
        print(f"Evidencia generada: {filename}")
