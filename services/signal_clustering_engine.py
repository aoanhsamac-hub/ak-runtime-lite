from __future__ import annotations

from typing import Any

from memory.learning_registry.schemas import SignalClusterRecord, CLUSTER_TYPES


CLUSTER_TYPE_MAP: dict[str, str] = {
    "DECISION": "DECISION",
    "TRADING": "TRADING",
    "RISK": "RISK",
    "EXECUTION": "EXECUTION",
    "GOVERNANCE": "GOVERNANCE",
    "ENGINEERING": "ENGINEERING",
    "MEMORY": "MEMORY",
}


class SignalClusteringEngine:
    """Groups learning signals into clusters by type and domain.

    Input: Learning Signals (from LearningSignalRegistry)
    Output: Signal Clusters (stored in SignalClusterRegistry)
    """

    def __init__(self, signal_registry, cluster_registry):
        self.signal_registry = signal_registry
        self.cluster_registry = cluster_registry

    def cluster_by_type(self, owner_agent: str = "Sage") -> list[SignalClusterRecord]:
        signals = self.signal_registry.list_all()
        type_groups: dict[str, list] = {}
        for sig in signals:
            mapped = self._map_signal_type_to_cluster(sig.signal_type)
            type_groups.setdefault(mapped, []).append(sig)

        clusters: list[SignalClusterRecord] = []
        for ctype, sigs in type_groups.items():
            if not sigs or ctype not in CLUSTER_TYPES:
                continue
            signal_ids = [s.signal_id for s in sigs]
            avg_conf = sum(s.confidence_score for s in sigs) / len(sigs)
            domains = set()
            for s in sigs:
                for tag in s.tags:
                    if tag not in ("lesson", "trace", "skill", "dataset",
                                   "pattern", "anomaly", "governance",
                                   "repeatable", "decision", "trading",
                                   "execution", "risk", "performance"):
                        domains.add(tag)
            cluster = self.cluster_registry.create_cluster(
                cluster_type=ctype,
                title=f"{ctype} Cluster ({len(sigs)} signals)",
                description=f"Cluster of {len(sigs)} {ctype.lower()} signals across {len(domains) or 'multiple'} domains",
                source_signal_ids=signal_ids,
                signal_count=len(sigs),
                confidence_score=round(avg_conf, 2),
                evidence={"domain_count": len(domains), "domains": list(domains)},
                owner_agent=owner_agent,
                tags=[ctype.lower(), "cluster"] + list(domains),
            )
            clusters.append(cluster)
        return clusters

    def cluster_by_domain(self, owner_agent: str = "Sage") -> list[SignalClusterRecord]:
        signals = self.signal_registry.list_all()
        domain_groups: dict[str, list] = {}
        for sig in signals:
            for tag in sig.tags:
                if tag not in ("lesson", "trace", "skill", "dataset",
                               "pattern", "anomaly", "governance",
                               "repeatable", "decision", "trading",
                               "execution", "risk", "performance",
                               "cluster", "consolidated", "emerging",
                               "gap", "risk", "governance"):
                    domain_groups.setdefault(tag, []).append(sig)

        clusters: list[SignalClusterRecord] = []
        for domain, sigs in domain_groups.items():
            if len(sigs) < 2:
                continue
            signal_ids = [s.signal_id for s in sigs]
            avg_conf = sum(s.confidence_score for s in sigs) / len(sigs)
            ctype = self._domain_to_cluster_type(domain)
            cluster = self.cluster_registry.create_cluster(
                cluster_type=ctype,
                title=f"Domain Cluster: {domain} ({len(sigs)} signals)",
                description=f"Cluster of {len(sigs)} signals in domain '{domain}'",
                source_signal_ids=signal_ids,
                signal_count=len(sigs),
                confidence_score=round(avg_conf, 2),
                evidence={"domain": domain, "signal_types": list({s.signal_type for s in sigs})},
                owner_agent=owner_agent,
                tags=[ctype.lower(), "domain_cluster", domain],
            )
            clusters.append(cluster)
        return clusters

    def run_all(self, owner_agent: str = "Sage") -> list[SignalClusterRecord]:
        clusters = self.cluster_by_type(owner_agent)
        clusters.extend(self.cluster_by_domain(owner_agent))
        return clusters

    @staticmethod
    def _map_signal_type_to_cluster(signal_type: str) -> str:
        m = {
            "PATTERN": "ENGINEERING",
            "ANOMALY": "RISK",
            "REPEATABILITY": "MEMORY",
            "GOVERNANCE": "GOVERNANCE",
            "DATASET": "ENGINEERING",
            "DECISION": "DECISION",
            "EXECUTION": "EXECUTION",
            "RISK": "RISK",
            "TRADING": "TRADING",
            "PERFORMANCE": "MEMORY",
        }
        return m.get(signal_type, "ENGINEERING")

    @staticmethod
    def _domain_to_cluster_type(domain: str) -> str:
        d = domain.lower().replace(" ", "_")
        if "trade" in d or "market" in d:
            return "TRADING"
        if "risk" in d or "security" in d or "governance" in d:
            return "RISK"
        if "exec" in d:
            return "EXECUTION"
        if "memory" in d:
            return "MEMORY"
        if "engineer" in d:
            return "ENGINEERING"
        if "agent" in d:
            return "DECISION"
        return "GOVERNANCE"
