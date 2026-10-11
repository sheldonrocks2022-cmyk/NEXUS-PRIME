import unittest
from nexus_prime.server import Handler

class LocalRequestTests(unittest.TestCase):
    def request(self, host, origin=""):
        obj = object.__new__(Handler)
        obj.headers = {"Host": host, "Origin": origin}
        return obj.trusted_request()

    def test_local_host(self):
        self.assertTrue(self.request("127.0.0.1:8765", "http://127.0.0.1:8765"))
        self.assertTrue(self.request("localhost:8765"))
    def test_remote_host_rejected(self):
        self.assertFalse(self.request("evil.example:8765"))
    def test_cross_origin_rejected(self):
        self.assertFalse(self.request("localhost:8765", "https://evil.example"))
