import os
import tempfile
import unittest
from unittest.mock import patch
from nexus_prime.core import Coordinator
from nexus_prime.memory import Memory

class IntegrationTests(unittest.TestCase):
    def test_mission_survives_reopening_database(self):
        with tempfile.TemporaryDirectory() as directory:
            path = os.path.join(directory, "missions.sqlite")
            mission = Coordinator().create("Improve the dashboard", "forge")
            Memory(path).save_mission(mission)
            saved = Memory(path).list_missions()
            self.assertEqual(saved[0]["id"], mission.id)
            self.assertEqual(saved[0]["agent"], "forge")

    def test_project_note_isolation(self):
        with tempfile.TemporaryDirectory() as directory:
            db = Memory(os.path.join(directory, "notes.sqlite"))
            db.add_note("alpha", "secret-free design")
            self.assertEqual(db.search_notes("beta"), [])
            self.assertEqual(db.search_notes("alpha"), ["secret-free design"])
