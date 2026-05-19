# Arquitectura del agente

## Componentes

- **Interfaz:** `app.py`, responsable de recibir consultas desde consola.
- **Agente:** `src/agent.py`, encargado de orquestar el flujo mediante LangGraph.
- **Herramientas:** `src/tools.py`, funciones autónomas que ejecutan acciones específicas.
- **Recuperación semántica:** `src/semantic_retriever.py`, encargado de construir y consultar el índice vectorial.
- **Memoria:** `src/memory.py`, responsable de persistir conversación y casos.
- **Planificación:** `src/planner.py`, secuencia tareas según prioridad y decisión.
- **Política de decisión:** `src/decision_policy.py`, define reglas de acción.
- **Tickets:** `src/ticket_writer.py`, registra casos que requieren seguimiento.

## Entrada y salida

Entrada:

```text
Consulta del usuario
```

Salida:

```text
Respuesta del agente + plan ejecutado + ticket si corresponde
```

## Persistencia

- `storage/vector_db`: índice semántico local.
- `storage/memory`: memoria conversacional y memoria de casos.
- `storage/tickets`: tickets generados por el agente.
