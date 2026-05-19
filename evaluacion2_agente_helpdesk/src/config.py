from pathlib import Path
from dotenv import load_dotenv
import os

load_dotenv()

PROJECT_ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = PROJECT_ROOT / "data" / "knowledge_base"
STORAGE_DIR = PROJECT_ROOT / "storage"
VECTOR_DB_DIR = Path(os.getenv("CHROMA_DIR", STORAGE_DIR / "vector_db"))
MEMORY_DIR = Path(os.getenv("MEMORY_DIR", STORAGE_DIR / "memory"))
TICKET_FILE = Path(os.getenv("TICKET_FILE", STORAGE_DIR / "tickets" / "tickets.jsonl"))

AGENT_NAME = os.getenv("AGENT_NAME", "Agente Helpdesk IA")
DEFAULT_USER_ID = os.getenv("DEFAULT_USER_ID", "usuario_demo")
EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL", "sentence-transformers/all-MiniLM-L6-v2")

CONFIDENCE_HIGH = float(os.getenv("CONFIDENCE_HIGH", "0.62"))
CONFIDENCE_MEDIUM = float(os.getenv("CONFIDENCE_MEDIUM", "0.42"))

for path in [DATA_DIR, VECTOR_DB_DIR, MEMORY_DIR, TICKET_FILE.parent]:
    Path(path).mkdir(parents=True, exist_ok=True)
