import unittest
from nexus_prime.orchestrator import Orchestrator

class OrchestratorTests(unittest.TestCase):
    def test_template_pipeline(self):
        output = Orchestrator().run("Build an app")
        self.assertEqual(len(output["steps"]), 6)
        self.assertEqual(output["status"], "approval_required")
        self.assertFalse(output["external_actions_executed"])
        self.assertEqual(output["steps"][0]["agent"], "prime")
    def test_ai_delegation(self):
        calls = []
        def fake(goal, agent, context):
            calls.append((agent, context))
            return "plan for " + agent
        output = Orchestrator(fake).run("Build an app", use_ai=True, max_agents=3)
        self.assertEqual(len(calls), 3)
        self.assertIn("plan for prime", calls[1][1])
        self.assertEqual(output["mode"], "ai")
    def test_invalid_limits(self):
        for count in (0, 7, True):
            with self.assertRaises(ValueError):
                Orchestrator().run("Build an app", max_agents=count)
    def test_empty_goal(self):
        with self.assertRaises(ValueError):
            Orchestrator().run("  ")
    def test_ai_error_is_not_hidden_as_success(self):
        def fail(*args):
            raise RuntimeError("provider unavailable")
        result = Orchestrator(fail).run("Investigate", use_ai=True, max_agents=1)
        self.assertEqual(result["steps"][0]["status"], "error")
