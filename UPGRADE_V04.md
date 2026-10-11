# NEXUS PRIME v0.4: multi-agent orchestration

The `nexus_prime.orchestrator.Orchestrator` runs a bounded six-stage planning pipeline:
PRIME → ARCHIVE → FORGE → SENTINEL → VERIFY → LAUNCH.

Each stage receives the mission and a bounded excerpt of previous stages' outputs.
In template mode it generates role assignments; with `use_ai=True` and a configured model it requests AI planning for each stage.
Provider errors are recorded on individual steps. Outputs remain proposals, with approval-required status.
No tools execute, no files are written, and no deployments occur.

This version includes unit tests. The next step is connecting orchestration to the dashboard API and adding persistence, tool permissions, and a human approval workflow.
