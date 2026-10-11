"""Bounded multi-agent mission orchestration.

Agent plans are proposals only; no generated code is executed.
"""
from dataclasses import dataclass, asdict
from uuid import uuid4
from .core import AGENTS
from .intelligence import reason

STAGES = (
    ("prime", "Clarify the goal, requirements, constraints, and acceptance criteria."),
    ("archive", "Identify relevant project context, assumptions, and missing information."),
    ("forge", "Propose an implementation plan, files, interfaces, and migration steps."),
    ("sentinel", "Review the proposed approach for security, permissions, and data risks."),
    ("verify", "Define deterministic tests, failure cases, and validation checks."),
    ("launch", "Create a safe rollout and rollback checklist; do not deploy."),
)

@dataclass
class AgentStep:
    agent: str
    objective: str
    output: str
    status: str = "completed"

class Orchestrator:
    def __init__(self, ai_callable=None):
        self.ai = ai_callable or reason

    def run(self, goal: str, *, use_ai=False, context="", max_agents=6):
        if not isinstance(goal, str) or not 1 <= len(goal.strip()) <= 4000:
            raise ValueError("Mission goal must be 1-4000 characters")
        if not isinstance(context, str) or len(context) > 12000:
            raise ValueError("Context must be at most 12000 characters")
        if type(max_agents) is not int or not 1 <= max_agents <= 6:
            raise ValueError("max_agents must be 1-6")
        steps = []
        for agent, objective in STAGES[:max_agents]:
            if use_ai:
                try:
                    output = self.ai(
                        "Mission: " + goal + "\nAssigned objective: " + objective +
                        "\nReturn a concise, actionable plan, not a claim of execution.",
                        agent,
                        context[:6000] + "\nEarlier agent proposals:\n" +
                        "\n".join(s.agent + ": " + s.output[:1000] for s in steps)[-6000:],
                    )
                    status = "completed"
                except Exception:
                    output = "AI planning unavailable for this step; no action was executed."
                    status = "error"
            else:
                output = "Planning assignment: " + objective + " Mission: " + goal
                status = "draft"
            steps.append(AgentStep(agent, objective, output, status))
        return {
            "id": uuid4().hex,
            "goal": goal,
            "status": "approval_required",
            "mode": "ai" if use_ai else "template",
            "steps": [asdict(step) for step in steps],
            "summary": "\n\n".join(
                "[" + step.agent.upper() + "] " + step.output for step in steps
            ),
            "external_actions_executed": False,
        }
