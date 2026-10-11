# NEXUS PRIME v0.2 modules
- SQLite mission and note storage via `nexus_prime.memory.Memory`.
- Optional HTTPS OpenAI-compatible model reasoning via `nexus_prime.intelligence.reason`.
- Public GitHub repository metadata inspection via `nexus_prime.github_intel.inspect`.
- Unit tests for persistence, model configuration, and input validation.

These modules are independently usable but are **not yet wired into the dashboard/server**. No autonomous coding, deployments, or external write operations are implemented. Configure API credentials via environment variables locally; do not commit secrets. Public GitHub inspection requires internet connectivity.
