#!/usr/bin/env python3
from __future__ import annotations

import json
import os
import platform
import subprocess
import sys
import webbrowser
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import urlparse

import refresh_skills


BASE_DIR = Path(__file__).resolve().parent
HOST = "127.0.0.1"
START_PORT = 8765


def open_folder(path: Path) -> bool:
    folder = path if path.is_dir() else path.parent
    system = platform.system().lower()
    try:
        if system == "windows":
            os.startfile(str(folder))  # type: ignore[attr-defined]
        elif system == "darwin":
            subprocess.run(["open", str(folder)], check=False)
        else:
            subprocess.run(["xdg-open", str(folder)], check=False)
        return True
    except Exception:
        return False


class Handler(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(BASE_DIR), **kwargs)

    def log_message(self, format: str, *args) -> None:
        return

    def send_json(self, status: int, payload: dict) -> None:
        body = json.dumps(payload, ensure_ascii=False).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self) -> None:
        if urlparse(self.path).path == "/api/status":
            self.send_json(200, {"ok": True})
            return
        super().do_GET()

    def do_POST(self) -> None:
        route = urlparse(self.path).path
        if route == "/api/refresh":
            data = refresh_skills.collect()
            payload = json.dumps(data, ensure_ascii=False, indent=2)
            (BASE_DIR / "skills-data.js").write_text(f"window.SKILL_DATA = {payload};\n", encoding="utf-8")
            self.send_json(200, data)
            return

        if route == "/api/open-folder":
            length = int(self.headers.get("Content-Length", "0") or "0")
            raw = self.rfile.read(length).decode("utf-8") if length else "{}"
            try:
                payload = json.loads(raw)
            except json.JSONDecodeError:
                self.send_json(400, {"ok": False, "error": "JSON 无效"})
                return
            target = Path(str(payload.get("path", ""))).expanduser()
            if not target.exists():
                self.send_json(404, {"ok": False, "error": "路径不存在"})
                return
            ok = open_folder(target)
            self.send_json(200 if ok else 500, {"ok": ok, "folder": str(target if target.is_dir() else target.parent)})
            return

        self.send_json(404, {"ok": False, "error": "未知接口"})


def make_server() -> tuple[ThreadingHTTPServer, int]:
    for port in range(START_PORT, START_PORT + 20):
        try:
            return ThreadingHTTPServer((HOST, port), Handler), port
        except OSError:
            continue
    server = ThreadingHTTPServer((HOST, 0), Handler)
    return server, int(server.server_address[1])


def ensure_initial_data() -> None:
    data = refresh_skills.collect()
    payload = json.dumps(data, ensure_ascii=False, indent=2)
    (BASE_DIR / "skills-data.js").write_text(f"window.SKILL_DATA = {payload};\n", encoding="utf-8")


def main() -> None:
    ensure_initial_data()
    server, port = make_server()
    url = f"http://{HOST}:{port}/index.html"
    print(f"Agent Skill Dashboard started: {url}")
    print("Close this window to stop the local service.")
    if "--no-browser" not in sys.argv and os.environ.get("AGENT_SKILL_DASHBOARD_NO_BROWSER") != "1":
        webbrowser.open(url)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()


if __name__ == "__main__":
    try:
        main()
    except Exception as exc:
        print(f"Failed to start: {exc}", file=sys.stderr)
        raise
