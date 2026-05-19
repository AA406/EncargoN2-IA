from src.agent import HelpdeskAgent
from src.config import DEFAULT_USER_ID


def main():
    agent = HelpdeskAgent()
    print("Agente Helpdesk Inteligente - EP2")
    print("Escribe una consulta o 'salir' para terminar.\n")

    while True:
        user_input = input("Usuario: ").strip()
        if user_input.lower() in {"salir", "exit", "quit"}:
            print("Sesión finalizada.")
            break
        if not user_input:
            continue
        result = agent.run(user_input, user_id=DEFAULT_USER_ID)
        agent.print_result(result)
        print("\n" + "-" * 70 + "\n")


if __name__ == "__main__":
    main()
