import unittest
from nexus_prime.core import Coordinator, Status, AGENTS

class MissionTests(unittest.TestCase):
    def test_agents(self):
        self.assertEqual(len(AGENTS), 8)
    def test_mission_requires_approval(self):
        c = Coordinator()
        m = c.create("Check a project", "phantom")
        self.assertEqual(m.status, Status.PENDING)
        c.plan(m.id)
        self.assertEqual(m.status, Status.APPROVAL)
        self.assertIn("request approval", m.result)
    def test_invalid_inputs(self):
        c = Coordinator()
        for goal, agent in [("", "prime"), ("hello", "unknown")]:
            with self.assertRaises(ValueError):
                c.create(goal, agent)

if __name__ == "__main__":
    unittest.main()
