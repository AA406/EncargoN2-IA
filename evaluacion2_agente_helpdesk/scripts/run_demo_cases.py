from src.agent import HelpdeskAgent

CASES = [
    "Olvidé mi contraseña y no puedo ingresar al sistema.",
    "Necesito conectarme por VPN desde mi casa y no me funciona el acceso remoto.",
    "El sistema de ventas está caído y nadie puede facturar, es urgente.",
    "Recibí un correo sospechoso que parece phishing y pide mis credenciales.",
    "Tengo un error raro que no aparece en ningún manual y necesito ayuda.",
]

if __name__ == "__main__":
    agent = HelpdeskAgent()
    for idx, case in enumerate(CASES, 1):
        print(f"\n\n===== CASO DEMO {idx} =====")
        print(f"Consulta: {case}")
        result = agent.run(case, user_id="demo_ep2")
        agent.print_result(result)
