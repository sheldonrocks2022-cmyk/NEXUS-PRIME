"""Dependency-free, permission-aware mission coordinator."""
from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from uuid import uuid4

class Status(str, Enum):
    PENDING = "pending"
    APPROVAL = "approval_required"
    COMPLETED = "completed"

@dataclass
class Mission:
    goal: str
    agent: str
    id: str = field(default_factory=lambda: uuid4().hex)
    status: Status = Status.PENDING
    created_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    result: str = ""

AGENTS = {
    "prime": "Coordinate and plan missions",
    "forge": "Plan code changes",
    "sentinel": "Review security risks",
    "phantom": "Diagnose errors",
    "verify": "Plan tests",
    "atlas": "Inspect GitHub work",
    "archive": "Organize project knowledge",
    "launch": "Prepare release checklists",
}

class Coordinator:
    def __init__(self):
        self.missions = {}

    def create(self, goal: str, agent: str = "prime") -> Mission:
        goal = goal.strip()
        if not goal or len(goal) > 4000:
            raise ValueError("Goal must be 1-4000 characters")
        if agent not in AGENTS:
            raise ValueError("Unknown agent")
        mission = Mission(goal=goal, agent=agent)
        self.missions[mission.id] = mission
        return mission

    def plan(self, mission_id: str) -> Mission:
        mission = self.missions[mission_id]
        mission.result = (
            f"Agent {mission.agent.upper()} received: {mission.goal}\n"
            "Next: inspect context, draft a plan, run checks, and request approval "
            "before writing files, deploying, or taking external actions."
        )
        mission.status = Status.APPROVAL
        return mission
