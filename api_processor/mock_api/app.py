from http.server import BaseHTTPRequestHandler, HTTPServer
import json
import time


HOST = "127.0.0.1"
PORT = 8001


class MockAPIHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        if self.path == "/users":
            users = [
                {
                    "id": 1,
                    "name": "Arun",
                    "email": "arun@example.com"
                },
                {
                    "id": "abc",
                    "name": "Sidhu",
                    "email": "sidhu@example.com"
                },
                {
                    "id": 3,
                    "name": "Hari",
                    "email": "hari@example.com"
                }
            ]
            for i in range(4, 501):
             users.append({
            "id": i,
            "name": f"User{i}",
            "email": f"user{i}@example.com"
       })
            response = json.dumps(users).encode("utf-8")

            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.send_header("Content-Length", str(len(response)))
            self.end_headers()

            self.wfile.write(response)      

        elif self.path == "/error":
            response = json.dumps({
                "error": "Internal Server Error"
            }).encode("utf-8")
            self.send_response(500)
            self.send_header("Content-Type", "application/json")
            self.send_header("Content-Length",str(len(response)))
            self.end_headers()
            self.wfile.write(response)

        elif self.path == "/slow":
            time.sleep(5)

            response = json.dumps({
               "message": "Slow response"
            }).encode("utf-8")

            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.send_header("Content-Length", str(len(response)))
            self.end_headers()

            self.wfile.write(response)

        else:
            response = json.dumps({
                "error": "Endpoint not found"
            }).encode("utf-8")

            self.send_response(404)
            self.send_header("Content-Type", "application/json")
            self.send_header("Content-Length", str(len(response)))
            self.end_headers()

            self.wfile.write(response)


def start_server():
    server = HTTPServer((HOST, PORT), MockAPIHandler)

    print(f"Mock API running at http://{HOST}:{PORT}")
    print("Available endpoint: /users")

    server.serve_forever()


if __name__ == "__main__":
    start_server()