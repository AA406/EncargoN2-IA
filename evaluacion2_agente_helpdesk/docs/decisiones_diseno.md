# Justificación de decisiones de diseño

## 1. Uso de LangGraph

Se utiliza LangGraph para representar el comportamiento del agente como un flujo de estados. Esta decisión permite dividir el proceso en etapas claras: carga de memoria, clasificación, recuperación semántica, decisión, acción y persistencia. Esta separación facilita la escalabilidad y la mantención del sistema.

## 2. Uso de LangChain Tools

Las herramientas del agente se declaran con la interfaz de LangChain Tools. Esto permite que cada acción sea modular, reutilizable y documentada. Las herramientas implementadas son consulta semántica, evaluación de prioridad, resumen de caso, creación de ticket y derivación humana.

## 3. Uso de ChromaDB y embeddings

La recuperación de información se implementa mediante embeddings y ChromaDB. Esta elección permite buscar documentos por significado y no solo por coincidencia exacta de palabras. Es adecuada para un Helpdesk porque los usuarios pueden describir el mismo problema con distintas palabras.

## 4. Memoria corta y larga

La memoria corta registra los últimos mensajes de cada usuario para sostener el contexto conversacional. La memoria larga registra casos y decisiones, permitiendo evidenciar continuidad en flujos prolongados y reutilización de información histórica.

## 5. Política de decisión

El agente no responde automáticamente todos los casos. Usa una política basada en prioridad, confianza y tipo de incidente. Si el caso es crítico, de seguridad o de baja confianza, crea ticket y deriva a soporte humano. Esto reduce el riesgo de entregar una respuesta incorrecta en situaciones sensibles para la operación.

## 6. Formato JSONL para tickets y memoria

JSONL permite registrar eventos de forma incremental y fácil de auditar. Cada línea representa un evento o ticket independiente, lo que facilita revisar evidencias sin depender de una base de datos externa.

## 7. Alineación con el flujo organizacional

El diseño responde al flujo típico de una mesa de ayuda: recepción de solicitud, clasificación, búsqueda de información, resolución inicial, escalamiento y registro. Por eso las herramientas seleccionadas se relacionan directamente con los requerimientos del proceso automatizado.
