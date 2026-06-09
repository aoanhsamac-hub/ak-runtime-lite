from __future__ import annotations

from typing import Any

from memory.learning_registry.schemas import InsightRecord, CLUSTER_TYPES


INSIGHT_TYPE_MAP: dict[str, str] = {
    "DECISION": "PROCESS",
    "TRADING": "MARKET",
    "RISK": "RISK",
    "EXECUTION": "EXECUTION",
    "GOVERNANCE": "GOVERNANCE",
    "ENGINEERING": "SKILL",
    "MEMORY": "PERFORMANCE",
}


class InsightDiscoveryEngine:
    """V2 insight discovery from signal clusters.

    Produces high-quality insights with evidence weighting,
    confidence scoring, and duplicate suppression.
    """

    def __init__(self, signal_registry, cluster_registry, insight_registry):
        self.signal_registry = signal_registry
        self.cluster_registry = cluster_registry
        self.insight_registry = insight_registry

    def discover_from_clusters(self, owner_agent: str = "Sage") -> list[InsightRecord]:
        clusters = self.cluster_registry.list_all()
        seen_signatures: set[str] = set()
        insights: list[InsightRecord] = []

        for cluster in clusters:
            insight_type = INSIGHT_TYPE_MAP.get(cluster.cluster_type, "SKILL")
            signature = f"{insight_type}:{cluster.title}"
            if signature in seen_signatures:
                continue
            seen_signatures.add(signature)

            evidence = dict(cluster.evidence)
            evidence["source_cluster_id"] = cluster.cluster_id
            evidence["source_signal_count"] = cluster.signal_count
            evidence["cluster_type"] = cluster.cluster_type

            insight = self.insight_registry.create_candidate(
                insight_type=insight_type,
                title=cluster.title,
                description=f"Discovered from {cluster.cluster_type} cluster: {cluster.description}",
                source_signal_ids=list(cluster.source_signal_ids),
                confidence_score=cluster.confidence_score,
                evidence=evidence,
                owner_agent=owner_agent,
                risk_level=cluster.risk_level,
                tags=[insight_type.lower(), "discovered"] + list(cluster.tags),
                metadata={"source_cluster_id": cluster.cluster_id, "discovery_engine": "V2"},
            )
            insights.append(insight)

        return insights

    def discover_from_signals_direct(self, owner_agent: str = "Sage") -> list[InsightRecord]:
        signals = self.signal_registry.list_all()
        type_groups: dict[str, list] = {}
        for sig in signals:
            type_groups.setdefault(sig.signal_type, []).append(sig)

        seen_signatures: set[str] = set()
        insights: list[InsightRecord] = []

        for sig_type, sigs in type_groups.items():
            if len(sigs) < 2:
                continue
            signal_ids = [s.signal_id for s in sigs]
            avg_conf = sum(s.confidence_score for s in sigs) / len(sigs)
            insight_type = self._signal_type_to_insight_type(sig_type)
            title = f"Direct Insight: {sig_type} ({len(sigs)} signals)"
            signature = f"{insight_type}:{title}"
            if signature in seen_signatures:
                continue
            seen_signatures.add(signature)

            domains = set()
            for s in sigs:
                for tag in s.tags:
                    if tag not in ("lesson", "trace", "skill", "dataset",
                                   "pattern", "anomaly", "governance",
                                   "repeatable", "decision", "trading",
                                   "execution", "risk", "performance"):
                        domains.add(tag)

            insight = self.insight_registry.create_candidate(
                insight_type=insight_type,
                title=title,
                description=f"Direct insight from {len(sigs)} {sig_type} signals across {len(domains) or 'multiple'} domains",
                source_signal_ids=signal_ids,
                confidence_score=round(avg_conf, 2),
                evidence={"signal_type": sig_type, "signal_count": len(sigs), "domains": list(domains)},
                owner_agent=owner_agent,
                tags=[insight_type.lower(), "direct"] + list(domains),
                metadata={"discovery_engine": "V2", "method": "direct"},
            )
            insights.append(insight)

        return insights

    def run_all(self, owner_agent: str = "Sage") -> list[InsightRecord]:
        insights = self.discover_from_clusters(owner_agent)
        insights.extend(self.discover_from_signals_direct(owner_agent))
        return insights

    @staticmethod
    def _signal_type_to_insight_type(signal_type: str) -> str:
        m = {
            "PATTERN": "SKILL", "ANOMALY": "RISK",
            "REPEATABILITY": "PERFORMANCE", "GOVERNANCE": "GOVERNANCE",
            "DATASET": "PROCESS", "DECISION": "PROCESS",
            "EXECUTION": "EXECUTION", "RISK": "RISK",
            "TRADING": "MARKET", "PERFORMANCE": "PERFORMANCE",
        }
        return m.get(signal_type, "SKILL")
