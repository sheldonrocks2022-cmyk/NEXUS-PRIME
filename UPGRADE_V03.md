# NEXUS PRIME v0.3 — Integrated Command Center

Run `python -m nexus_prime.server` and open http://127.0.0.1:8765.

## Connected features
- Mission plans are now saved to SQLite and survive restarts.
- Dashboard has project memory notes, with per-project retrieval.
- Dashboard can inspect public GitHub repository metadata (read-only).
- Dashboard has optional AI planning, activated per mission, using the v0.2 model adapter.
- Health endpoint: GET /api/health.

## Configure optional AI
Set `NEXUS_API_KEY` and `NEXUS_MODEL` as environment variables. The default endpoint uses the OpenAI-compatible chat completions API. Do not commit credentials or expose the local dashboard to the internet.

## Security and limitations
The dashboard is bound to 127.0.0.1 and has no authentication. It does not execute model-proposed code, modify GitHub, or deploy anything. The approval-required status is informational; an approval execution engine is not implemented. AI responses may be inaccurate and are not verified. Public repository inspection requires network access. SQLite is stored at `nexus_prime.db` unless `NEXUS_DB_PATH` is set. Do not put sensitive project secrets into memory notes.

## Next
Add authenticated remote access, bounded agent orchestration, permission-scoped tools, workflow inspection, explicit approval state transitions, and end-to-end tests.
