# Flujo de trabajo del agente

## Flujo principal

1. El usuario ingresa una solicitud de soporte.
2. El agente carga memoria reciente para mantener continuidad.
3. La solicitud se clasifica por categoría: acceso, conectividad, software, hardware, seguridad, RR.HH. o general.
4. Se evalúa prioridad: normal, alta o crítica.
5. Se recupera contexto semántico desde la base de conocimiento.
6. Se calcula un nivel de confianza a partir de la similitud del contexto recuperado.
7. La política de decisión determina la acción:
   - responder con contexto;
   - responder y crear ticket;
   - crear ticket y derivar a humano.
8. El agente ejecuta la acción correspondiente.
9. Se guarda el caso en memoria de corto y largo plazo.

## Condiciones adaptativas

| Condición | Acción del agente |
|---|---|
| Confianza alta y prioridad normal | Responde con información recuperada. |
| Confianza media | Responde, pero crea ticket preventivo. |
| Confianza baja | Crea ticket y deriva a soporte humano. |
| Prioridad crítica | Crea ticket y deriva inmediatamente. |
| Seguridad / phishing | Entrega orientación inicial y deriva. |

## Ejemplo de flujo

Consulta: "El sistema de ventas está caído y nadie puede facturar".

Resultado:

- Categoría: software.
- Prioridad: crítica.
- Acción: crear ticket y derivar humano.
- Justificación: impacto operacional alto.
