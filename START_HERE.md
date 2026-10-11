# NEXUS PRIME v0.1
A local-first mission command center with eight named agent roles, mission planning, a browser dashboard, and GitHub Actions tests.

## Run on Windows
1. Install Python 3.12 or newer.
2. Download and extract this repository.
3. Open PowerShell in the extracted directory.
4. Run `python -m nexus_prime.server`.
5. Open http://127.0.0.1:8765

No API keys or external dependencies required.

## Current limitations
This is an initial working scaffold, **not** autonomous AI yet. Agents are role definitions; missions produce deterministic approval-gated plans. Missions are stored in memory and disappear when the server restarts. GitHub Actions currently runs unit tests, not deployments. The HTTP server binds to localhost only and is not authenticated; do not expose it publicly.

## Next milestones
Add SQLite persistence, AI provider adapters, permission-scoped tool execution, GitHub repository inspection, approval workflow, and comprehensive tests.
