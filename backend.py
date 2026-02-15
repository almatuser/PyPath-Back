import json
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import parse_qs, urlparse

BASE_DIR = Path(__file__).resolve().parent
DB_PATH = BASE_DIR / "db.json"
SWAGGER_PATH = BASE_DIR / "swagger.json"

with DB_PATH.open(encoding="utf-8") as db_file:
    DATA = json.load(db_file)


def _json_response(handler: BaseHTTPRequestHandler, status: int, payload):
    raw = json.dumps(payload, ensure_ascii=False).encode("utf-8")
    handler.send_response(status)
    handler.send_header("Content-Type", "application/json; charset=utf-8")
    handler.send_header("Content-Length", str(len(raw)))
    handler.send_header("Access-Control-Allow-Origin", "*")
    handler.end_headers()
    handler.wfile.write(raw)


def _read_json_body(handler: BaseHTTPRequestHandler):
    size = int(handler.headers.get("Content-Length", 0))
    if size <= 0:
        return {}
    if size > 1024 * 1024:
        raise ValueError("Payload too large")
    body = handler.rfile.read(size)
    return json.loads(body.decode("utf-8"))


class PyPathHandler(BaseHTTPRequestHandler):
    def do_OPTIONS(self):
        self.send_response(204)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET,POST,PUT,OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type, Authorization, X-API-Key")
        self.end_headers()

    def do_GET(self):
        parsed = urlparse(self.path)
        path = parsed.path
        query = parse_qs(parsed.query)

        if path == "/swagger.json":
            with SWAGGER_PATH.open(encoding="utf-8") as swagger_file:
                return _json_response(self, 200, json.load(swagger_file))

        if path in {"/currentUser", "/stats", "/activity", "/skills", "/friends", "/uiData", "/logs", "/missions"}:
            return _json_response(self, 200, DATA[path[1:]])
        if path == "/courses":
            return _json_response(self, 200, DATA["courses"])
        if path.startswith("/courses/"):
            return self._get_by_id("courses", path.split("/", 2)[2], parse_int=True)
        if path == "/leaderboard":
            items = DATA["leaderboard"]
            scope = (query.get("scope", [""])[0] or "").lower()
            if scope == "friends":
                items = [row for row in items if row.get("isFriend")]
            elif scope == "school":
                items = [row for row in items if row.get("isSchool")]
            return _json_response(self, 200, items)
        if path == "/posts":
            posts = DATA["posts"][:]
            tag = query.get("tag", [None])[0]
            if tag:
                tag_lc = tag.lower()
                posts = [post for post in posts if any(t.lower() == tag_lc for t in post.get("tags", []))]
            sort = (query.get("sort", [""])[0] or "").lower()
            if sort == "popular":
                posts.sort(key=lambda post: post.get("likes", 0), reverse=True)
            elif sort == "fresh":
                posts.sort(key=lambda post: post.get("id", 0), reverse=True)
            return _json_response(self, 200, posts)
        if path == "/achievements":
            achievements = DATA["achievements"]
            category = query.get("category", [None])[0]
            if category:
                category_lc = category.lower()
                achievements = [a for a in achievements if str(a.get("category", "")).lower() == category_lc]
            return _json_response(self, 200, achievements)
        if path.startswith("/missions/"):
            mission_id = path.split("/", 2)[2]
            if "/" in mission_id:
                return self._not_found()
            return self._get_by_id("missions", mission_id, parse_int=False)

        return self._not_found()

    def do_PUT(self):
        if urlparse(self.path).path != "/currentUser":
            return self._not_found()

        try:
            payload = _read_json_body(self)
        except (ValueError, json.JSONDecodeError):
            return _json_response(self, 400, {"error": "Invalid JSON payload"})

        DATA["currentUser"].update(payload)
        return _json_response(self, 200, DATA["currentUser"])

    def do_POST(self):
        path = urlparse(self.path).path

        if path == "/posts":
            try:
                payload = _read_json_body(self)
            except (ValueError, json.JSONDecodeError):
                return _json_response(self, 400, {"error": "Invalid JSON payload"})

            content = str(payload.get("content", "")).strip()
            if not content:
                return _json_response(self, 400, {"error": "Field 'content' is required"})

            posts = DATA["posts"]
            next_id = max((post.get("id", 0) for post in posts), default=0) + 1
            new_post = {
                "id": next_id,
                "author": {
                    "name": DATA["currentUser"].get("name", "User"),
                    "avatar": DATA["currentUser"].get("avatar"),
                    "level": DATA["currentUser"].get("levelNum", 1),
                },
                "time": "только что",
                "content": content,
                "code": payload.get("code"),
                "tags": payload.get("tags", []),
                "likes": 0,
                "comments": 0,
                "liked": False,
            }
            posts.append(new_post)
            return _json_response(self, 201, new_post)

        if path.startswith("/posts/") and path.endswith("/like"):
            post_id = path[len("/posts/") : -len("/like")].strip("/")
            for post in DATA["posts"]:
                if str(post.get("id")) == post_id:
                    post["likes"] = post.get("likes", 0) + 1
                    post["liked"] = True
                    return _json_response(self, 200, post)
            return self._not_found()

        if path.startswith("/missions/") and path.endswith("/submit"):
            mission_id = path[len("/missions/") : -len("/submit")].strip("/")
            mission = next((item for item in DATA["missions"] if str(item.get("id")) == mission_id), None)
            if mission is None:
                return self._not_found()
            try:
                payload = _read_json_body(self)
            except (ValueError, json.JSONDecodeError):
                return _json_response(self, 400, {"error": "Invalid JSON payload"})

            code = str(payload.get("code", "")).strip()
            if not code:
                return _json_response(self, 400, {"error": "Field 'code' is required"})

            return _json_response(
                self,
                200,
                {
                    "success": True,
                    "message": "Решение отправлено успешно",
                    "xpEarned": mission.get("xpReward", 0),
                },
            )

        return self._not_found()

    def _get_by_id(self, bucket: str, raw_id: str, parse_int: bool):
        if parse_int:
            try:
                raw_id = int(raw_id)
            except ValueError:
                return self._not_found()

        item = next((value for value in DATA[bucket] if value.get("id") == raw_id), None)
        if item is None:
            return self._not_found()
        return _json_response(self, 200, item)

    def _not_found(self):
        return _json_response(self, 404, {"error": "Not found"})

    def log_message(self, format, *args):
        return


if __name__ == "__main__":
    server = ThreadingHTTPServer(("0.0.0.0", 3000), PyPathHandler)
    print("PyPath backend is running on http://localhost:3000")
    server.serve_forever()
