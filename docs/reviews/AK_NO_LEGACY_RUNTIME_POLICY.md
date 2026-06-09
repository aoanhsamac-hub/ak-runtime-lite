# Alkasik Kingdom No Legacy Runtime Policy

## Policy

AK must not import direct code from Alkasik Legacy.

AK must not use Legacy runtime paths, databases, dashboards, API gateways, config loaders, bot scripts, trading scripts, or connector code.

Legacy is a knowledge and archive source only.

Strategy logic from Legacy may move into AK only as lessons, specifications, requirements, or reviewed design records. Runtime code must not be copied.

Files missing required metadata must be placed into quarantine until reviewed.

Every migration must record source, hash, owner, reviewer, and status.

Legacy may be archived only after AK passes the Replacement Gate.

## Enforcement

- Governance review is required before any migration.
- Execution must fail-closed when governance state is invalid.
- Secrets, API keys, credentials, and passwords must not be printed or written into reports.
