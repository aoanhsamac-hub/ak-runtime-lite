from memory.agent_memory import AgentMemoryClient, agent_memory_client
from memory.lancedb_adapter import LanceDBAdapter
from memory.memory_interface import MemoryInterface

from tests.test_lancedb_adapter import FakeBackend


def test_all_ak_agents_can_receive_memory_clients_without_direct_backend_access(tmp_path):
    interface = MemoryInterface(adapter=LanceDBAdapter(tmp_path, backend=FakeBackend()))

    for agent_id in ["janus", "sage", "hermes", "iris", "helen", "lang_lieu", "yet_kieu"]:
        client = agent_memory_client(agent_id, interface)
        assert isinstance(client, AgentMemoryClient)
        assert client.agent_id in {"Janus", "Sage", "Hermes", "Iris", "Helen", "LangLieu", "YetKieu"}
        assert not hasattr(client, "backend")


def test_agent_memory_client_records_decision_through_interface(tmp_path):
    interface = MemoryInterface(adapter=LanceDBAdapter(tmp_path, backend=FakeBackend()))
    client = agent_memory_client("lang_lieu", interface)

    trace = client.record_decision(
        decision="Use MemoryInterface",
        reasoning="Agents must not write LanceDB directly.",
        evidence=["WP3 prompt", "memory interface contract"],
        outcome="Decision trace recorded.",
    )

    assert trace.agent == "LangLieu"
    assert trace.evidence == ["WP3 prompt", "memory interface contract"]
