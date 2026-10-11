"""Persistent proposal review. Approval never executes a proposed action."""
from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from threading import RLock
from uuid import uuid4
import json
import sqlite3

ACTIONS = {"inspect_repository": "low", "propose_patch": "medium", "open_pull_request": "high", "deploy": "critical"}
DECISIONS = {"approved", "rejected"}

def now():
    return datetime.now(timezone.utc).isoformat()

@dataclass
class Proposal:
    action: str
    summary: str
    target: str
    id: str = field(default_factory=lambda: uuid4().hex)
    risk: str = ""
    status: str = "pending"
    created_at: str = field(default_factory=now)
    decided_at: str = ""

class Governance:
    def __init__(self, path="nexus_prime.db"):
        self.path = str(path)
        self.lock = RLock()
        with self.connect() as db:
            db.execute("CREATE TABLE IF NOT EXISTS proposals (id TEXT PRIMARY KEY, payload TEXT NOT NULL)")
            db.execute("CREATE TABLE IF NOT EXISTS proposal_events (id INTEGER PRIMARY KEY, proposal_id TEXT NOT NULL, event TEXT NOT NULL, created_at TEXT NOT NULL)")

    def connect(self):
        return sqlite3.connect(self.path, timeout=10)

    def submit(self, action, summary, target):
        if action not in ACTIONS:
            raise ValueError("Unsupported action")
        if not isinstance(summary, str) or not 1 <= len(summary.strip()) <= 2000:
            raise ValueError("Invalid summary")
        if not isinstance(target, str) or not 1 <= len(target.strip()) <= 300:
            raise ValueError("Invalid target")
        proposal = Proposal(action=action, summary=summary.strip(), target=target.strip(), risk=ACTIONS[action])
        with self.lock, self.connect() as db:
            db.execute("INSERT INTO proposals VALUES (?,?)", (proposal.id, json.dumps(asdict(proposal))))
            db.execute("INSERT INTO proposal_events(proposal_id,event,created_at) VALUES (?,?,?)", (proposal.id, "submitted", now()))
        return asdict(proposal)

    def list(self):
        with self.lock, self.connect() as db:
            rows = db.execute("SELECT payload FROM proposals ORDER BY rowid DESC LIMIT 200").fetchall()
        return [json.loads(row[0]) for row in rows]

    def decide(self, proposal_id, decision):
        if decision not in DECISIONS:
            raise ValueError("Invalid decision")
        with self.lock, self.connect() as db:
            row = db.execute("SELECT payload FROM proposals WHERE id=?", (proposal_id,)).fetchone()
            if row is None:
                raise KeyError("Proposal not found")
            proposal = json.loads(row[0])
            if proposal["status"] != "pending":
                raise ValueError("Proposal already decided")
            proposal["status"] = decision
            proposal["decided_at"] = now()
            db.execute("UPDATE proposals SET payload=? WHERE id=?", (json.dumps(proposal), proposal_id))
            db.execute("INSERT INTO proposal_events(proposal_id,event,created_at) VALUES (?,?,?)", (proposal_id, decision, now()))
            return proposal

    def events(self, proposal_id):
        with self.lock, self.connect() as db:
            rows = db.execute("SELECT event,created_at FROM proposal_events WHERE proposal_id=? ORDER BY id", (proposal_id,)).fetchall()
        return [{"event": event, "created_at": timestamp} for event, timestamp in rows]
