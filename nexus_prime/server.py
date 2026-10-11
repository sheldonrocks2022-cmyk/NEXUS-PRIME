"""Local-only HTTP API and dashboard; no external actions."""
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
import json
from .core import AGENTS, Coordinator

coordinator = Coordinator()
DASHBOARD = Path(__file__).with_name("dashboard.html").read_bytes()

class Handler(BaseHTTPRequestHandler):
    def respond(self, code, payload):
        data = json.dumps(payload).encode()
        self.send_response(code)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(data)))
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(data)

    def do_GET(self):
        if self.path == "/":
            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.send_header("Content-Length", str(len(DASHBOARD)))
            self.end_headers()
            self.wfile.write(DASHBOARD)
        elif self.path == "/api/agents":
            self.respond(200, {"agents": AGENTS})
        elif self.path == "/api/missions":
            self.respond(200, {"missions": [vars(m) for m in coordinator.missions.values()]})
        else:
            self.respond(404, {"error": "Not found"})

    def do_POST(self):
        if self.path != "/api/missions":
            return self.respond(404, {"error": "Not found"})
        try:
            size = int(self.headers.get("Content-Length", "0"))
            if size < 1 or size > 8192:
                return self.respond(413, {"error": "Invalid request size"})
            body = json.loads(self.rfile.read(size))
            mission = coordinator.create(body["goal"], body.get("agent", "prime"))
            coordinator.plan(mission.id)
            self.respond(201, {"mission": vars(mission)})
        except (ValueError, KeyError, TypeError, json.JSONDecodeError) as exc:
            self.respond(400, {"error": str(exc)})

def main():
    print("NEXUS PRIME ready at http://127.0.0.1:8765")
    ThreadingHTTPServer(("127.0.0.1", 8765), Handler).serve_forever()

if __name__ == "__main__":
    main()
