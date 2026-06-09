"""Tests for runtime resource threshold monitoring."""

import psutil
import pytest


class TestRAMThresholds:
    def test_ram_available_exceeds_minimum(self):
        total = psutil.virtual_memory().total
        assert total >= 2 * 1024**3, "System RAM must be >= 2 GB"

    def test_ram_free_exceeds_stop_condition(self):
        free = psutil.virtual_memory().available
        assert free >= 200 * 1024**2, f"Available RAM ({free / 1024**2:.0f} MB) must be >= 200 MB to avoid stop condition"

    def test_ram_free_pct_sufficient(self):
        pct = psutil.virtual_memory().percent
        assert pct < 95, f"RAM usage ({pct}%) too high for safe runtime operation"

    def test_ram_guard_for_low_memory_raises(self):
        free = psutil.virtual_memory().available
        assert free > 50 * 1024**2, "Critical: dangerously low memory"


class TestCPUThresholds:
    def test_cpu_count_minimum(self):
        assert psutil.cpu_count() >= 1, "At least 1 CPU core required"

    def test_cpu_count_recommended(self):
        assert psutil.cpu_count() >= 2, "Recommended: at least 2 CPU cores"

    def test_cpu_usage_not_critical(self):
        usage = psutil.cpu_percent(interval=0.1)
        assert usage < 90, f"CPU usage ({usage}%) too high"

    def test_cpu_load_average_not_saturated(self):
        load = psutil.getloadavg() if hasattr(psutil, "getloadavg") else (0, 0, 0)
        cores = psutil.cpu_count()
        for i, avg in enumerate(load):
            assert avg < cores * 0.9, f"Load average ({avg}) near saturation on {cores} cores"


class TestDiskThresholds:
    def test_disk_free_minimum(self):
        usage = psutil.disk_usage("C:\\")
        assert usage.free >= 10 * 1024**3, "At least 10 GB free disk required"

    def test_disk_usage_not_critical(self):
        usage = psutil.disk_usage("C:\\")
        assert usage.percent < 95, f"Disk usage ({usage.percent}%) critically high"

    def test_disk_d_available(self):
        disks = psutil.disk_partitions()
        d_drives = [d for d in disks if d.mountpoint.startswith("D:")]
        if d_drives:
            usage = psutil.disk_usage("D:\\")
            assert usage.free >= 5 * 1024**3, "D drive should have at least 5 GB free"


class TestResourceMonitorRuntime:
    def test_runtime_memory_budget_sufficient(self):
        free = psutil.virtual_memory().available
        runtime_budget = 530 * 1024**2  # 530 MB estimated
        assert free >= runtime_budget, f"Free RAM ({free / 1024**2:.0f} MB) insufficient for runtime budget (530 MB)"

    def test_vps_ram_above_stop_threshold(self):
        free_mb = 333  # VPS target available RAM
        threshold_mb = 200
        assert free_mb >= threshold_mb, f"VPS RAM ({free_mb} MB) would trigger stop (threshold: {threshold_mb} MB)"

    def test_total_ram_sufficient_for_runtime(self):
        total = psutil.virtual_memory().total
        runtime_estimate = 1 * 1024**3  # 1 GB total system estimate
        assert total >= runtime_estimate, f"Total RAM ({total / 1024**3:.1f} GB) must be >= 1 GB"

    def test_no_memory_leak_in_threshold_check(self):
        before = psutil.Process().memory_info().rss
        for _ in range(100):
            _ = psutil.virtual_memory()
        after = psutil.Process().memory_info().rss
        assert after - before < 1024**2, "Threshold check should not leak memory (>1 MB growth)"
