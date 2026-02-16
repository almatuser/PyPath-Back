import json
import threading
import time
import unittest
from http.client import HTTPConnection
from http.server import ThreadingHTTPServer
from json import JSONDecodeError

import backend


class BackendAPITestCase(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.server = ThreadingHTTPServer(("127.0.0.1", 0), backend.PyPathHandler)
        cls.port = cls.server.server_address[1]
        cls.thread = threading.Thread(target=cls.server.serve_forever, daemon=True)
        cls.thread.start()
        time.sleep(0.05)

    @classmethod
    def tearDownClass(cls):
        cls.server.shutdown()
        cls.server.server_close()
        cls.thread.join(timeout=2)

    def request(self, method, path, body=None):
        conn = HTTPConnection("127.0.0.1", self.port)
        payload = None
        headers = {}
        if body is not None:
            payload = json.dumps(body)
            headers["Content-Type"] = "application/json"
        conn.request(method, path, payload, headers)
        res = conn.getresponse()
        raw = res.read().decode("utf-8")
        conn.close()
        try:
            parsed = json.loads(raw) if raw else {}
        except JSONDecodeError:
            parsed = {}
        return res.status, parsed

    def test_get_course_by_id(self):
        status, payload = self.request("GET", "/courses/1")
        self.assertEqual(status, 200)
        self.assertEqual(payload["id"], 1)

    def test_get_achievements_with_category_filter(self):
        status, payload = self.request("GET", "/achievements?category=streak")
        self.assertEqual(status, 200)
        self.assertTrue(payload)
        self.assertTrue(all(item["category"] == "streak" for item in payload))

    def test_create_post_requires_content(self):
        status, payload = self.request("POST", "/posts", {"tags": ["Python"]})
        self.assertEqual(status, 400)
        self.assertIn("content", payload["error"])

    def test_get_achievements_category_all_returns_everything(self):
        status, all_items = self.request("GET", "/achievements")
        self.assertEqual(status, 200)
        status, filtered = self.request("GET", "/achievements?category=all")
        self.assertEqual(status, 200)
        self.assertEqual(len(filtered), len(all_items))

    def test_get_leaderboard_with_scope_friends(self):
        status, all_items = self.request("GET", "/leaderboard")
        self.assertEqual(status, 200)
        status, payload = self.request("GET", "/leaderboard?scope=friends")
        self.assertEqual(status, 200)
        self.assertTrue(all(item.get("isFriend") for item in payload))
        self.assertLessEqual(len(payload), len(all_items))

    def test_get_leaderboard_with_period(self):
        status, payload = self.request("GET", "/leaderboard?period=month")
        self.assertEqual(status, 200)
        self.assertIsInstance(payload, list)

    def test_submit_mission(self):
        status, missions = self.request("GET", "/missions")
        self.assertEqual(status, 200)
        mission_id = missions[0]["id"]
        status, payload = self.request("POST", f"/missions/{mission_id}/submit", {"code": "print('ok')"})
        self.assertEqual(status, 200)
        self.assertTrue(payload["success"])
        self.assertIn("xpEarned", payload)


if __name__ == "__main__":
    unittest.main()
