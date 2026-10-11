"""Local-only command center with persistent missions and optional AI planning."""
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import urlsplit, parse_qs
import json
import os
from .core import AGENTS, Coordinator
from .memory import Memory
from .intelligence import reason
from .github_intel import inspect
from .orchestrator import Orchestrator
from .governance import Governance

coordinator = Coordinator()
memory = Memory(os.getenv("NEXUS_DB_PATH", "nexus_prime.db"))
governance = Governance(os.getenv("NEXUS_DB_PATH", "nexus_prime.db"))
DASHBOARD = Path(__file__).with_name("dashboard.html").read_bytes()

class Handler(BaseHTTPRequestHandler):
    def respond(self, code, payload):
        data = json.dumps(payload).encode()
        self.send_response(code)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(data)))
        self.send_header("Cache-Control", "no-store")
        self.send_header("X-Content-Type-Options", "nosniff")
        self.end_headers()
        self.wfile.write(data)

    def trusted_request(self):
        host = self.headers.get("Host", "")
        origin = self.headers.get("Origin", "")
        return host in ("127.0.0.1:8765", "localhost:8765") and (not origin or origin in ("http://127.0.0.1:8765", "http://localhost:8765"))

    def do_GET(self):
        if not self.trusted_request():
            return self.respond(403, {"error": "Local requests only"})
        parsed = urlsplit(self.path)
        if parsed.path == "/":
            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.send_header("Content-Length", str(len(DASHBOARD)))
            self.send_header("Cache-Control", "no-store")
            self.end_headers()
            self.wfile.write(DASHBOARD)
        elif parsed.path == "/api/agents":
            self.respond(200, {"agents": AGENTS})
        elif parsed.path == "/api/missions":
            self.respond(200, {"missions": memory.list_missions()})
        elif parsed.path == "/api/notes":
            params = parse_qs(parsed.query)
            project = params.get("project", [""])[0][:100]
            query = params.get("query", [""])[0][:200]
            self.respond(200, {"notes": memory.search_notes(project, query)})
        elif parsed.path == "/api/proposals":
            self.respond(200, {"proposals": governance.list()})
        elif parsed.path == "/api/health":
            self.respond(200, {"status": "ready", "agents": len(AGENTS), "ai_configured": bool(os.getenv("NEXUS_API_KEY") and os.getenv("NEXUS_MODEL"))})
        else:
            self.respond(404, {"error": "Not found"})

    def do_POST(self):
        if not self.trusted_request():
            return self.respond(403, {"error": "Local requests only"})
        path = urlsplit(self.path).path
        if path not in ("/api/missions", "/api/notes", "/api/github", "/api/orchestrate", "/api/proposals", "/api/decisions"):
            return self.respond(404, {"error": "Not found"})
        try:
            size = int(self.headers.get("Content-Length", "0"))
            if size < 1 or size > 8192:
                return self.respond(413, {"error": "Invalid request size"})
            body = json.loads(self.rfile.read(size))
            if not isinstance(body, dict):
                raise ValueError("Expected JSON object")
            if path == "/api/proposals":
                return self.respond(201, {"proposal": governance.submit(body["action"], body["summary"], body["target"])})
            if path == "/api/decisions":
                return self.respond(200, {"proposal": governance.decide(body["id"], body["decision"])})
            if path == "/api/missions":
                mission = coordinator.create(body["goal"], body.get("agent", "prime"))
                coordinator.plan(mission.id)
                if body.get("use_ai") is True:
                    try:
                        mission.result = reason(mission.goal, mission.agent, str(body.get("context", ""))[:12000])
                    except Exception:
                        mission.result = "AI provider request failed. No external action was performed."
                memory.save_mission(mission)
                return self.respond(201, {"mission": vars(mission)})
            if path == "/api/orchestrate":
                result = Orchestrator().run(body["goal"], use_ai=body.get("use_ai") is True, context=body.get("context", ""), max_agents=body.get("max_agents", 6))
                return self.respond(200, {"orchestration": result})
            if path == "/api/notes":
                memory.add_note(body["project"][:100], body["body"])
                return self.respond(201, {"saved": True})
            if path == "/api/github":
                return self.respond(200, {"repository": inspect(body["owner"], body["repo"])})
        except (ValueError, TypeError, json.JSONDecodeError) as exc:
            self.respond(400, {"error": str(exc)})
        except KeyError as exc:
            self.respond(400, {"error": "Missing field or proposal: " + str(exc)})
            self.respond(400, {"error": str(exc)})
        except Exception:
            self.respond(502, {"error": "External read failed"})

def main():
    print("NEXUS PRIME ready at http://127.0.0.1:8765")
    ThreadingHTTPServer(("127.0.0.1", 8765), Handler).serve_forever()

if __name__ == "__main__":
    main()
