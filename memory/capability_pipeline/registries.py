from __future__ import annotations

from typing import Any
from memory.capability_pipeline.schemas import (
    CapabilityCandidateRecord,
    CapabilityFamilyRecord,
    CanonicalCapabilityRecord,
    PromotionRecommendationRecord,
)


class CapabilityCandidateRegistry:
    table_name = "capability_candidates"

    def __init__(self, adapter=None):
        self.adapter = adapter
        self._records: dict[str, CapabilityCandidateRecord] = {}

    def create(self, **payload) -> CapabilityCandidateRecord:
        record = CapabilityCandidateRecord(**payload)
        self._records[record.capability_id] = record
        if self.adapter:
            self.adapter.insert(self.table_name, [record.to_dict()])
        return record

    def get(self, capability_id: str) -> CapabilityCandidateRecord:
        try:
            return self._records[capability_id]
        except KeyError as exc:
            raise KeyError(f"capability not found: {capability_id}") from exc

    def list_all(self, domain: str | None = None) -> list[CapabilityCandidateRecord]:
        records = list(self._records.values())
        if domain:
            records = [r for r in records if r.domain == domain]
        return records


class CapabilityFamilyRegistry:
    table_name = "capability_families"

    def __init__(self, adapter=None):
        self.adapter = adapter
        self._records: dict[str, CapabilityFamilyRecord] = {}

    def create(self, **payload) -> CapabilityFamilyRecord:
        record = CapabilityFamilyRecord(**payload)
        self._records[record.family_id] = record
        if self.adapter:
            self.adapter.insert(self.table_name, [record.to_dict()])
        return record

    def get(self, family_id: str) -> CapabilityFamilyRecord:
        try:
            return self._records[family_id]
        except KeyError as exc:
            raise KeyError(f"family not found: {family_id}") from exc

    def list_all(self) -> list[CapabilityFamilyRecord]:
        return list(self._records.values())


class CanonicalCapabilityRegistry:
    table_name = "canonical_capabilities"

    def __init__(self, adapter=None):
        self.adapter = adapter
        self._records: dict[str, CanonicalCapabilityRecord] = {}

    def create(self, **payload) -> CanonicalCapabilityRecord:
        record = CanonicalCapabilityRecord(**payload)
        self._records[record.canonical_id] = record
        if self.adapter:
            self.adapter.insert(self.table_name, [record.to_dict()])
        return record

    def get(self, canonical_id: str) -> CanonicalCapabilityRecord:
        try:
            return self._records[canonical_id]
        except KeyError as exc:
            raise KeyError(f"canonical capability not found: {canonical_id}") from exc

    def list_all(self, classification: str | None = None) -> list[CanonicalCapabilityRecord]:
        records = list(self._records.values())
        if classification:
            records = [r for r in records if r.classification == classification]
        return records


class PromotionRecommendationRegistry:
    table_name = "promotion_recommendations"

    def __init__(self, adapter=None):
        self.adapter = adapter
        self._records: dict[str, PromotionRecommendationRecord] = {}

    def create(self, **payload) -> PromotionRecommendationRecord:
        record = PromotionRecommendationRecord(**payload)
        self._records[record.recommendation_id] = record
        if self.adapter:
            self.adapter.insert(self.table_name, [record.to_dict()])
        return record

    def list_all(self, decision: str | None = None) -> list[PromotionRecommendationRecord]:
        records = list(self._records.values())
        if decision:
            records = [r for r in records if r.decision == decision]
        return records
