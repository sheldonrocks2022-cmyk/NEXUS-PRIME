import os
import tempfile
import unittest
from unittest.mock import patch
from nexus_prime.memory import Memory
from nexus_prime.intelligence import reason
from nexus_prime.github_intel import inspect

class AdvancedTests(unittest.TestCase):
    def test_persistent_memory(self):
        with tempfile.TemporaryDirectory() as tmp:
            path=os.path.join(tmp,"db.sqlite")
            db=Memory(path)
            db.add_note("project","critical build error")
            self.assertEqual(Memory(path).search_notes("project","BUILD"),["critical build error"])
    def test_unconfigured_ai(self):
        with patch.dict(os.environ,{"NEXUS_API_KEY":"","NEXUS_MODEL":""}):
            self.assertIn("not configured",reason("hello"))
    def test_invalid_github_identifier(self):
        with self.assertRaises(ValueError):
            inspect("../secrets","repo")
if __name__=="__main__":
    unittest.main()
