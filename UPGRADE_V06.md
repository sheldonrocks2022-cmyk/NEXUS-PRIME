# NEXUS PRIME v0.6 — Approval Command Center

The dashboard now exposes proposal creation, review, approval, and rejection through local HTTP endpoints:
- GET /api/proposals
- POST /api/proposals with action, summary, target
- POST /api/decisions with id, decision

Decisions are stored persistently in the SQLite governance database. Proposals have immutable action categories and risk levels. Approval does not execute a tool, modify files, create a pull request, or deploy software.

The HTTP server is still intended for local single-user development. Basic Host and Origin checks mitigate browser cross-origin requests and DNS rebinding but **do not replace authentication**. Do not expose the server on a public interface. Before adding real execution tools, implement authenticated sessions, CSRF defenses, granular authorization, and reviewed action-specific scopes.
