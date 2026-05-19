from src.memory import ConversationMemory


def test_conversation_memory_tmp_path(tmp_path):
    memory = ConversationMemory(memory_dir=tmp_path)
    memory.append("user_test", "user", "hola")
    recent = memory.load_recent("user_test", limit=1)
    assert len(recent) == 1
    assert recent[0]["content"] == "hola"
