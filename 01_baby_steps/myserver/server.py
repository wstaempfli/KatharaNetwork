#!/usr/bin/env python3
import http.server
import socketserver
import argparse

class MyHandler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/plain')
        self.end_headers()
        self.wfile.write(b"Hello Tarrif$")

def main():
    parser = argparse.ArgumentParser(description="Simple HTTP server")
    parser.add_argument("port", nargs="?", type=int, default=8000)
    args = parser.parse_args()

    port = args.port

    # Server setup
    with socketserver.TCPServer(("0.0.0.0", port), MyHandler) as httpd:
        print(f"Serving at 0.0.0.0:{port}")
        httpd.serve_forever()

if __name__ == "__main__":
    main()