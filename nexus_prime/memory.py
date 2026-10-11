"""SQLite persistence for missions and knowledge notes."""
import json
import sqlite3
from pathlib import Path

class Memory:
    def __init__(self, path="nexus_prime.db"):
        self.path = str(path)
        with self.connect() as db:
            db.execute("CREATE TABLE IF NOT EXISTS missions (id TEXT PRIMARY KEY, payload TEXT NOT NULL)")
            db.execute("CREATE TABLE IF NOT EXISTS notes (id INTEGER PRIMARY KEY, project TEXT NOT NULL, body TEXT NOT NULL)")

    def connect(self):
        return sqlite3.connect(self.path, timeout=10)

    def save_mission(self, mission):
        with self.connect() as db:
            db.execute("INSERT OR REPLACE INTO missions VALUES (?,?)", (mission.id, json.dumps(vars(mission))))

    def list_missions(self):
        with self.connect() as db:
            rows = db.execute("SELECT payload FROM missions ORDER BY rowid DESC LIMIT 200").fetchall()
        return [json.loads(row[0]) for row in rows]

    def add_note(self, project, body):
        if not project.strip() or not body.strip() or len(body)>20000:
            raise ValueError("Invalid note")
        with self.connect() as db:
            db.execute("INSERT INTO notes (project,body) VALUES (?,?)", (project.strip(), body.strip()))

    def search_notes(self, project, query=""):
        with self.connect() as db:
            rows = db.execute("SELECT body FROM notes WHERE project=? AND instr(lower(body),lower(?))>0 ORDER BY id DESC LIMIT 20", (project, query)).fetchall()
        return [row[0] for row in rows]
