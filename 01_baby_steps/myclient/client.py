#!/usr/bin/env python3
import socket
import argparse

def main():
    parser = argparse.ArgumentParser(description="Simple HTTP client")
    parser.add_argument("server_ip")
    parser.add_argument("port", nargs="?", type=int, default=8000)
    args = parser.parse_args()

    ip = args.server_ip
    port = args.port

    # Create a TCP socket
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        # Connect to the server
        sock.connect((ip, port))
        
        # Send an HTTP GET request
        request = (
            f"GET / HTTP/1.1\r\n"
            f"Host: {ip}:{port}\r\n"
            f"Connection: close\r\n\r\n"
        )
        sock.send(request.encode())

        # Receive and parse the response
        response = b""
        while True:
            data = sock.recv(4096)  # Read in chunks
            if not data:
                break
            response += data

    # Decode and split headers/body
    response_str = response.decode()
    _, body = response_str.split("\r\n\r\n", 1)  # Split headers and body
    print(body.strip())

if __name__ == "__main__":
    main()