import os
import tempfile
import unittest
from nexus_prime.governance import Governance

class GovernanceTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.path = os.path.join(self.tmp.name, "governance.sqlite")
        self.gov = Governance(self.path)

    def test_persistent_approval(self):
        proposal = self.gov.submit("propose_patch", "Fix an issue", "repo/file.py")
        self.assertEqual(proposal["risk"], "medium")
        approved = Governance(self.path).decide(proposal["id"], "approved")
        self.assertEqual(approved["status"], "approved")
        self.assertEqual(len(self.gov.events(proposal["id"])), 2)

    def test_double_decision_rejected(self):
        proposal = self.gov.submit("deploy", "Release version", "production")
        self.gov.decide(proposal["id"], "rejected")
        with self.assertRaises(ValueError):
            self.gov.decide(proposal["id"], "approved")

    def test_unknown_action_rejected(self):
        with self.assertRaises(ValueError):
            self.gov.submit("execute_shell", "Do something", "server")

    def test_no_execution(self):
        proposal = self.gov.submit("deploy", "Deployment proposal", "production")
        self.gov.decide(proposal["id"], "approved")
        self.assertEqual(self.gov.list()[0]["status"], "approved")
        self.assertNotIn("executed", self.gov.list()[0])
