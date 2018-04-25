import json

from http.server import HTTPServer
from http.server import SimpleHTTPRequestHandler

from sgmon.task import TaskManager


class MonitorServer(SimpleHTTPRequestHandler):
    def do_GET(self):
        manager = TaskManager()
        if "/tasks" in self.path:
            self.send_response(200, "OK")
            self.send_header("Content-type", "text/json")
            self.end_headers()
            self.wfile.write(bytes(json.dumps(manager.get_tasks()),
                                   encoding="utf-8"))

        if "/health" in self.path:
            self.send_response(200, "OK")
            self.send_header("Content-type", "text/json")
            self.end_headers()
            self.wfile.write(bytes(json.dumps(
                {"data": {"monitor": {"result": "OK"},
                          "newrelic": {"result": "OK"}}}), encoding="utf-8"))


def serve_forever():
    server = HTTPServer(('', 8888), MonitorServer)
    server.serve_forever()
