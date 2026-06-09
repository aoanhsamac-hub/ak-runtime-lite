"""Agent status monitor for PSOP-02."""

from pathlib import Path


AGENTS_DIR = Path(__file__).resolve().parent.parent / "agents"

AGENT_NAMES = ["janus", "sage", "hermes", "iris", "helen", "lang_lieu", "yet_kieu"]

AGENT_TITLES = {
    "janus": "Executive Orchestrator",
    "sage": "Supreme Governance & Risk Court",
    "hermes": "Memory, Dataset, Documentation",
    "iris": "Economic & Market Intelligence",
    "helen": "Information & Civilization Intelligence",
    "lang_lieu": "Engineering & Architecture",
    "yet_kieu": "Security & Infrastructure",
}


def check():
    agents = []
    total_agents = len(AGENT_NAMES)
    active_agents = 0
    inactive_agents = 0

    for name in AGENT_NAMES:
        config_path = AGENTS_DIR / name / "agent.yaml"
        agent_path = AGENTS_DIR / name / "agent.py"

        config_exists = config_path.exists()
        agent_exists = agent_path.exists()

        status = "PRESENT" if config_exists and agent_exists else "MISSING_CONFIG"

        if config_exists:
            import yaml
            try:
                config = yaml.safe_load(config_path.read_text(encoding="utf-8"))
                mode = config.get(name, {}).get("mode", "unknown") if isinstance(config.get(name), dict) else "unknown"
                agent_status = config.get(name, {}).get("status", "unknown") if isinstance(config.get(name), dict) else "unknown"
            except Exception:
                mode = "error"
                agent_status = "error"
        else:
            mode = "unknown"
            agent_status = "unknown"

        agents.append({
            "name": name,
            "title": AGENT_TITLES.get(name, ""),
            "config_exists": config_exists,
            "agent_exists": agent_exists,
            "config_status": agent_status,
            "mode": mode,
            "agent_status": "OPERATIONAL" if agent_exists else "NOT_FOUND",
        })

        if agent_exists:
            active_agents += 1
        else:
            inactive_agents += 1

    active_pct = round(active_agents / total_agents * 100) if total_agents > 0 else 0

    if inactive_agents == 0:
        status = "HEALTHY"
        detail = f"All {total_agents} agents operational"
    elif inactive_agents <= 2:
        status = "WATCH"
        detail = f"{active_agents}/{total_agents} agents operational"
    else:
        status = "WARNING"
        detail = f"{active_agents}/{total_agents} agents operational"

    return {
        "status": status,
        "score": active_pct,
        "detail": detail,
        "agents": agents,
        "active_count": active_agents,
        "total_agents": total_agents,
    }
