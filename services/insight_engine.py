from __future__ import annotations

from typing import Any

from memory.learning_registry.schemas import InsightRecord


class InsightEngine:
    """Aggregates learning signals into insights.

    No autonomous learning — insights are recorded as CANDIDATE only.
    """

    def __init__(self, signal_registry, insight_registry):
        self.signal_registry = signal_registry
        self.insight_registry = insight_registry

    def consolidate_signals(self, owner_agent: str = "Sage") -> list[InsightRecord]:
        """Group signals by type into consolidated insights."""
        all_signals = self.signal_registry.list_all()
        insights: list[InsightRecord] = []

        type_groups: dict[str, list] = {}
        for sig in all_signals:
            type_groups.setdefault(sig.signal_type, []).append(sig)

        for sig_type, sigs in type_groups.items():
            if not sigs:
                continue
            signal_ids = [s.signal_id for s in sigs]
            avg_confidence = sum(s.confidence_score for s in sigs) / len(sigs)
            domains = set()
            for s in sigs:
                for tag in s.tags:
                    if tag not in ("lesson", "skill", "dataset", "trace", "pattern", "anomaly", "governance", "repeatable"):
                        domains.add(tag)
            title = f"Consolidated {sig_type} Signals ({len(sigs)} sources)"
            description = f"Aggregated {len(sigs)} {sig_type} signals across {len(domains) or 'multiple'} domains"

            insight = self.insight_registry.create_candidate(
                insight_type=self._map_signal_type_to_insight_type(sig_type),
                title=title,
                description=description,
                source_signal_ids=signal_ids,
                confidence_score=round(avg_confidence, 2),
                evidence={"source_count": len(sigs), "signal_types": [sig_type], "domains": list(domains)},
                owner_agent=owner_agent,
                tags=[sig_type.lower(), "consolidated"] + list(domains),
            )
            insights.append(insight)

        return insights

    def generate_trend_insight(self, owner_agent: str = "Sage") -> InsightRecord | None:
        """Generate a trend insight from PATTERN and REPEATABILITY signals."""
        pattern_signals = self.signal_registry.list_all(signal_type="PATTERN")
        repeat_signals = self.signal_registry.list_all(signal_type="REPEATABILITY")
        combined = pattern_signals + repeat_signals
        if not combined:
            return None
        avg_conf = sum(s.confidence_score for s in combined) / len(combined)
        signal_ids = [s.signal_id for s in combined]
        return self.insight_registry.create_candidate(
            insight_type="TREND",
            title=f"Emerging Trend ({len(combined)} signals)",
            description=f"Trend detected from {len(pattern_signals)} pattern and {len(repeat_signals)} repeatability signals",
            source_signal_ids=signal_ids,
            confidence_score=round(avg_conf, 2),
            evidence={"pattern_count": len(pattern_signals), "repeatability_count": len(repeat_signals)},
            owner_agent=owner_agent,
            tags=["trend", "emerging"],
        )

    def generate_gap_insight(self, owner_agent: str = "Sage") -> InsightRecord | None:
        """Generate a gap insight from ANOMALY signals."""
        anomaly_signals = self.signal_registry.list_all(signal_type="ANOMALY")
        if not anomaly_signals:
            return None
        avg_conf = sum(s.confidence_score for s in anomaly_signals) / len(anomaly_signals)
        signal_ids = [s.signal_id for s in anomaly_signals]
        return self.insight_registry.create_candidate(
            insight_type="GAP",
            title=f"Knowledge Gap ({len(anomaly_signals)} anomalies)",
            description=f"Gap detected from {len(anomaly_signals)} anomaly signals indicating failure patterns",
            source_signal_ids=signal_ids,
            confidence_score=round(avg_conf, 2),
            evidence={"anomaly_count": len(anomaly_signals)},
            owner_agent=owner_agent,
            tags=["gap", "anomaly"],
        )

    def generate_risk_insight(self, owner_agent: str = "Sage") -> InsightRecord | None:
        """Generate a risk insight from GOVERNANCE signals."""
        gov_signals = self.signal_registry.list_all(signal_type="GOVERNANCE")
        dataset_signals = self.signal_registry.list_all(signal_type="DATASET")
        combined = gov_signals + dataset_signals
        if not combined:
            return None
        avg_conf = sum(s.confidence_score for s in combined) / len(combined)
        signal_ids = [s.signal_id for s in combined]
        return self.insight_registry.create_candidate(
            insight_type="RISK",
            title=f"Risk Assessment ({len(combined)} signals)",
            description=f"Risk insight from {len(gov_signals)} governance and {len(dataset_signals)} dataset signals",
            source_signal_ids=signal_ids,
            confidence_score=round(avg_conf, 2),
            evidence={"governance_count": len(gov_signals), "dataset_count": len(dataset_signals)},
            owner_agent=owner_agent,
            tags=["risk", "governance"],
        )

    def run_all(self, owner_agent: str = "Sage") -> dict[str, list[InsightRecord]]:
        results: dict[str, list[InsightRecord]] = {
            "consolidated": self.consolidate_signals(owner_agent),
            "trends": [],
            "gaps": [],
            "risks": [],
        }
        trend = self.generate_trend_insight(owner_agent)
        if trend:
            results["trends"].append(trend)
        gap = self.generate_gap_insight(owner_agent)
        if gap:
            results["gaps"].append(gap)
        risk = self.generate_risk_insight(owner_agent)
        if risk:
            results["risks"].append(risk)
        return results

    @staticmethod
    def _map_signal_type_to_insight_type(signal_type: str) -> str:
        mapping = {
            "PATTERN": "PATTERN",
            "ANOMALY": "GAP",
            "REPEATABILITY": "PATTERN",
            "GOVERNANCE": "RISK",
            "DATASET": "CONSOLIDATION",
        }
        return mapping.get(signal_type, "CONSOLIDATION")
