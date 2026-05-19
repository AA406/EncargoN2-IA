# Evaluación Parcial 2



## 1. Objetivo 

Automatizar la atención inicial de consultas de soporte interno para una organización simulada llamada **Implementos**, permitiendo:

- Responder consultas frecuentes desde una base de conocimiento.
- Clasificar solicitudes de soporte.
- Recuperar contexto semántico mediante embeddings.
- Mantener continuidad con memoria de corto y largo plazo.
- Decidir si responde, crea ticket o deriva a soporte humano.
- Registrar evidencias de prueba para validar el comportamiento del agente.

---

## 2. Arquitectura

se compone de los siguientes módulos:

| Componente | Archivo | Función |
|---|---|---|
| Interfaz CLI | `app.py` | Permite ejecutar el agente desde consola. |
| Orquestador | `src/agent.py` | Coordina el flujo usando LangGraph. |
| Herramientas | `src/tools.py` | Expone funciones de consulta, ticket, prioridad y escalamiento. |
| Recuperador semántico | `src/semantic_retriever.py` | Indexa y consulta documentos usando ChromaDB y embeddings. |
| Memoria | `src/memory.py` | Guarda historial corto y casos en memoria persistente. |
| Planificador | `src/planner.py` | Secuencia las tareas según prioridad y estado. |
| Política de decisión | `src/decision_policy.py` | Define cuándo responder, crear ticket o escalar. |
| Registro de tickets | `src/ticket_writer.py` | Guarda tickets en formato JSONL. |

Diagrama principal disponible en:

```text
/docs/diagrama_orquestacion.mmd
```

---

## 3. Herramientas del agente

El agente incorpora herramientas específicas, compatibles con LangChain:

1. `consultar_base_conocimiento`: recupera información semántica desde documentos internos.
2. `evaluar_prioridad`: determina prioridad de la solicitud.
3. `resumir_caso`: resume el problema informado por el usuario.
4. `crear_ticket_soporte`: registra un ticket estructurado.
5. `derivar_a_humano`: genera una derivación cuando hay baja confianza o riesgo operativo.

Estas herramientas permiten demostrar autonomía funcional, ya que el agente decide cuál usar según la consulta.

---

## 4. Memoria y recuperación de contexto

El sistema usa dos niveles de memoria:

- **Memoria de corto plazo:** mantiene los últimos mensajes del usuario para dar continuidad a la conversación.
- **Memoria de largo plazo:** guarda casos relevantes y acciones tomadas para consultas futuras.

La recuperación semántica se implementa con:

- `sentence-transformers/all-MiniLM-L6-v2` para embeddings.
- `ChromaDB` como base vectorial local.
- Documentos Markdown dentro de `data/knowledge_base`.

---

## 5. Instalación local

Crear entorno virtual:

```bash
python -m venv .venv
```

Activar entorno:

```bash
# Windows
.venv\Scripts\activate

# Linux / macOS
source .venv/bin/activate
```

Instalar dependencias:

```bash
pip install -r requirements.txt
```

Copiar variables de entorno:

```bash
copy .env.example .env
```

En Linux/macOS:

```bash
cp .env.example .env
```

---

## 6. Indexar base de conocimiento

Antes de ejecutar el agente, se recomienda crear el índice semántico:

```bash
python scripts/ingest_knowledge_base.py
```

---

## 7. Ejecutar el agente

Modo interactivo:

```bash
python app.py
```

Modo demo con casos de prueba:

```bash
python scripts/run_demo_cases.py
```

Ejecutar pruebas:

```bash
pytest
```

---

## 8. Ejemplos de uso

### Caso 1: consulta simple

**Usuario:**

```text
Olvidé mi contraseña y no puedo ingresar al sistema.
```

**Comportamiento esperado:**

- Clasifica el caso como acceso/cuenta.
- Consulta documentos sobre recuperación de contraseña.
- Responde con pasos de solución.
- No crea ticket si la confianza es alta.

### Caso 2: incidente urgente

**Usuario:**

```text
El sistema de ventas está caído y nadie puede facturar.
```

**Comportamiento esperado:**

- Detecta prioridad crítica.
- Crea ticket automáticamente.
- Deriva a soporte humano.
- Guarda el caso en memoria.

### Caso 3: baja confianza

**Usuario:**

```text
Necesito solucionar un error raro que no aparece en ningún manual.
```

**Comportamiento esperado:**

- Recupera contexto insuficiente.
- Crea ticket por baja confianza.
- Indica que se requiere revisión humana.

---

## 9. Evidencias

Las evidencias se encuentran en la carpeta:

```text
evidencias/
```

Incluyen ejemplos de:

- Consulta resuelta automáticamente.
- Creación de ticket.
- Escalamiento humano.
- Uso de memoria contextual.

---

## 10. Relación con los indicadores de evaluación

| Indicador | Evidencia en el repositorio |
|---|---|
| IE1 | `src/tools.py` y ejecución de herramientas. |
| IE2 | Uso de LangGraph, LangChain Tools, ChromaDB y embeddings. |
| IE3 | `src/memory.py` con memoria de corto y largo plazo. |
| IE4 | `src/semantic_retriever.py` con recuperación semántica. |
| IE5 | `src/planner.py` con secuenciación de tareas. |
| IE6 | `evidencias/` y `scripts/run_demo_cases.py`. |
| IE7 | `README.md` y `docs/diagrama_orquestacion.mmd`. |
| IE8 | `docs/decisiones_diseno.md`. |
| IE9 | `docs/Informe_Tecnico_EP2.md` y diagramas. |
| IE10 | Redacción técnica y ejemplos concretos. |

---

## 11. Referencias

Las referencias APA están disponibles en:

```text
docs/referencias_apa.md
```
