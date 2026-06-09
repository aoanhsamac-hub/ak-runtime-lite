"""Runtime Daemon - Entry point that starts and keeps running all AK-RUNTIME-LITE services."""

import sys
import os
import time
import signal
import logging

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from services.telegram_gateway import TelegramGateway
from services.kingdom_scheduler import RuntimeScheduler
from services.runtime_supervisor import RuntimeSupervisor

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(name)s] %(levelname)s: %(message)s",
    handlers=[logging.StreamHandler()],
)
log = logging.getLogger("runtime_daemon")

RUNNING = True

def _signal_handler(signum, frame):
    global RUNNING
    log.info(f"Received signal {signum}, shutting down...")
    RUNNING = False

signal.signal(signal.SIGTERM, _signal_handler)
signal.signal(signal.SIGINT, _signal_handler)


def main():
    log.info("=== AK-RUNTIME-LITE DAEMON STARTING ===")

    telegram = TelegramGateway()
    scheduler = RuntimeScheduler()
    supervisor = RuntimeSupervisor()

    supervisor.register_component("telegram_gateway")
    supervisor.register_component("kingdom_scheduler")
    supervisor.register_component("runtime_supervisor")

    result_tg = telegram.start()
    log.info(f"TelegramGateway.start() -> {result_tg}")

    result_sched = scheduler.start()
    log.info(f"RuntimeScheduler.start() -> {result_sched}")

    result_sup = supervisor.start()
    log.info(f"RuntimeSupervisor.start() -> {result_sup}")

    supervisor.record_heartbeat("telegram_gateway")
    supervisor.record_heartbeat("kingdom_scheduler")
    supervisor.record_heartbeat("runtime_supervisor")

    log.info("=== DAEMON RUNNING (Ctrl+C to stop) ===")

    tick = 0
    while RUNNING:
        time.sleep(10)
        tick += 1
        if tick % 6 == 0:
            health = supervisor.status_report()
            log.info(f"Health: running={health['running']}, "
                     f"components={len(health['components'])}, "
                     f"all_healthy={health['all_healthy']}")

    telegram.stop()
    scheduler.stop()
    supervisor.stop()
    log.info("=== DAEMON STOPPED ===")


if __name__ == "__main__":
    main()
