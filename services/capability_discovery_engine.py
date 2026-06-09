from __future__ import annotations

from typing import Any
from memory.capability_pipeline.schemas import CAPABILITY_DOMAINS


DOMAIN_CATEGORY_MAP = {
    "Trading": ["trading", "market", "trade"],
    "Risk": ["risk", "anomaly", "security"],
    "Execution": ["execution", "workflow", "optimization", "monitoring"],
    "Governance": ["governance", "compliance", "policy", "audit"],
    "Memory": ["memory", "performance", "repeatability", "pattern", "retention", "consolidation"],
    "Engineering": ["engineering", "dataset", "signal", "pipeline", "recognition", "foundation"],
    "Agent": ["agent", "decision", "coordination", "delegation", "process"],
}


class CapabilityDiscoveryEngine:
    """Discovers capability candidates from approved skills + decision traces."""

    def __init__(self, approved_skill_registry, capability_registry, trace_registry=None):
        self.approved_skill_registry = approved_skill_registry
        self.capability_registry = capability_registry
        self.trace_registry = trace_registry

    def discover_from_skills(self, owner_agent: str = "Sage") -> list:
        skills = self.approved_skill_registry.list_all(status="ACTIVE")
        if not skills:
            skills = self.approved_skill_registry.list_all()
        seen_domains = set()
        capabilities = []

        for s in skills:
            domain = self._classify_domain(s)
            if domain not in seen_domains:
                seen_domains.add(domain)
                domain_skills = [x for x in skills if self._classify_domain(x) == domain]
                cap = self.capability_registry.create(
                    name=f"{domain} Capability",
                    description=f"Unified capability for {domain} domain from {len(domain_skills)} approved skills",
                    domain=domain,
                    source_skill_ids=[x.approved_skill_id for x in domain_skills],
                    confidence_score=round(sum(x.confidence_score for x in domain_skills) / max(len(domain_skills), 1), 2),
                    evidence={
                        "skill_count": len(domain_skills),
                        "avg_confidence": round(sum(x.confidence_score for x in domain_skills) / max(len(domain_skills), 1), 2),
                        "domain": domain,
                        "source": "approved_skills",
                    },
                    owner_agent=owner_agent,
                    tags=[domain.lower(), "capability", "discovered"],
                )
                capabilities.append(cap)
        return capabilities

    def discover_from_traces(self, owner_agent: str = "Sage") -> list:
        if not self.trace_registry:
            return []
        capabilities = []
        try:
            traces = self.trace_registry.list_all() if hasattr(self.trace_registry, 'list_all') else []
        except Exception:
            traces = []
        if not traces:
            return capabilities
        domain_traces = {}
        for t in traces:
            domain = self._classify_domain(t)
            domain_traces.setdefault(domain, []).append(t)
        for domain, trace_list in domain_traces.items():
            existing = self.capability_registry.list_all(domain=domain)
            if existing:
                continue
            cap = self.capability_registry.create(
                name=f"{domain} Trace Capability",
                description=f"Trace-derived capability for {domain} from {len(trace_list)} decision traces",
                domain=domain,
                source_trace_ids=[getattr(t, 'trace_id', '') for t in trace_list],
                confidence_score=0.70,
                evidence={
                    "trace_count": len(trace_list),
                    "domain": domain,
                    "source": "decision_traces",
                },
                owner_agent=owner_agent,
                tags=[domain.lower(), "capability", "trace-derived"],
            )
            capabilities.append(cap)
        return capabilities

    def run_all(self, owner_agent: str = "Sage") -> list:
        results = self.discover_from_skills(owner_agent)
        results += self.discover_from_traces(owner_agent)
        return results

    @staticmethod
    def _classify_domain(record) -> str:
        name = getattr(record, 'name', getattr(record, 'title', ''))
        desc = getattr(record, 'description', '')
        combined = (name + " " + desc).lower()
        for domain, keywords in DOMAIN_CATEGORY_MAP.items():
            for kw in keywords:
                if kw in combined:
                    return domain
        return "Engineering"
