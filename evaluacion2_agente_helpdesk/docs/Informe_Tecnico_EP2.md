# Informe técnico - Evaluación Parcial 2

## 1. Contexto y objetivo

El objetivo es implementar un agente funcional para una mesa de ayuda. Su objetivo es automatizar la atención inicial de solicitudes de soporte, recuperando información desde una base de conocimiento, manteniendo memoria de contexto y tomando decisiones sobre si responder, crear ticket o derivar a soporte humano.

## 2. Diseño e implementación del agente

El agente fue implementado en Python utilizando LangGraph para el flujo y LangChain Tools para definir herramientas. El flujo considera carga de memoria, clasificación de solicitud, recuperación semántica, evaluación de confianza, planificación de tareas, ejecución de acciones y persistencia del resultado.

Las herramientas configuradas son: consulta de base de conocimiento, evaluación de prioridad, resumen de caso, creación de ticket y derivación humana. Estas herramientas permiten que el agente ejecute funciones específicas según el estado de cada solicitud.

## 3. Memoria y recuperación de contexto

La memoria se divide en dos niveles. La memoria de corto plazo guarda los últimos mensajes del usuario para mantener continuidad conversacional. La memoria de largo plazo registra casos atendidos, categoría, prioridad, decisión tomada y ticket generado cuando corresponde.

La recuperación de contexto se realiza mediante embeddings con Sentence Transformers y una base vectorial local en ChromaDB. Este mecanismo permite recuperar documentos por similitud semántica, mejorando la respuesta frente a consultas expresadas con distintas palabras.

## 4. Planificación y toma de decisiones

El planificador secuencia las tareas del agente de acuerdo con prioridad y confianza. La política de decisión define tres rutas: responder con contexto cuando la confianza es alta, responder y crear ticket cuando la confianza es media, o crear ticket y derivar a humano cuando el caso es crítico o la confianza es baja.

Ejemplo: si el usuario indica que el sistema de ventas está caído y nadie puede facturar, el agente detecta prioridad crítica, genera ticket y deriva a soporte humano. En cambio, si el usuario olvidó su contraseña y existe documentación suficiente, responde con el procedimiento recuperado.

## 5. Evidencias y justificación técnica

El repositorio incluye evidencias de ejecución, casos de prueba, diagramas Mermaid y documentación técnica. Las decisiones de diseño se justifican por su alineación con el flujo de una mesa de ayuda: recibir solicitud, clasificar, recuperar información, decidir acción, registrar y escalar si corresponde.

La arquitectura seleccionada permite escalabilidad porque cada componente se encuentra separado por responsabilidad. También permite compatibilidad técnica porque utiliza herramientas ampliamente usadas en proyectos de agentes y recuperación aumentada por información.

## Referencias

Ver archivo `docs/referencias_apa.md`.
