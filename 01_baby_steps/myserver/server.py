#!/usr/bin/env python3
import http.server
import socketserver
import argparse

def main():
    parser = argparse.ArgumentParser(description="Simple HTTP server")
    parser.add_argument("port", nargs="?", type=int, default=8000)
    args = parser.parse_args()

    port = args.port

    ## TODO-03:  


if __name__ == "__main__":
    main()