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

    ## TODO-04: implement your HTTP client here


if __name__ == "__main__":
    main()