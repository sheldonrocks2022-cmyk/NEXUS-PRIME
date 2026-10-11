# NEXUS PRIME v0.5 — Mission Governance

New `nexus_prime.governance.Governance` module stores action proposals and an append-only event history in SQLite. Each proposal has a fixed action type, target, risk classification, and decision status. Decisions are one-time and recorded.

**Approval does not execute anything.** The module deliberately has no shell, GitHub write, deployment, or file-editing capabilities. It provides a review foundation for a future executor.

Supported proposal categories: inspect_repository, propose_patch, open_pull_request, deploy.

This module has unit tests but is not yet exposed by the HTTP dashboard. The existing localhost-only HTTP server has no authentication; do not expose a decision endpoint remotely without adding authentication, CSRF protections, and authorization checks.
