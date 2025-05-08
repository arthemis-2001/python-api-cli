#!/usr/bin/env python3

"""
Usage: file-client [options] stat UUID
       file-client [options] read UUID
       file-client --help

Subcommands:
  stat                  Prints the file metadata in a human-readable manner.
  read                  Outputs the file content.

Options:
  --help                Show this help message and exit.
  --backend=BACKEND     Set a backend to be used, choices are grpc and rest. Default is grpc.
  --grpc-server=NETLOC  Set a host and port of the gRPC server. Default is localhost:50051.
  --base-url=URL        Set a base URL for a REST server. Default is http://localhost/.
  --output=OUTPUT       Set the file where to store the output. Default is -, i.e. the stdout.
"""

import sys
import argparse
import requests
from typing import *
from urllib.parse import urljoin


def _fetch_data(backend: str, uuid: str, url: str) -> Optional[requests.Response]:
    if backend == "grpc":
        raise NotImplementedError("grpc backend not implemented")
    else:
        try:
            response = requests.get(url, timeout=5)

            if response.status_code == 200:
                return response

            elif response.status_code == 400:
                print(f"Bad request.", file=sys.stderr)
            elif response.status_code == 401:
                print(f"Authorization required.", file=sys.stderr)
            elif response.status_code == 403:
                print(f"Access forbidden.", file=sys.stderr)
            elif response.status_code == 404:
                print(f"File under {uuid} not found.", file=sys.stderr)
            elif response.status_code >= 500:
                print(f"Server error.", file=sys.stderr)
        except requests.exceptions.ConnectionError:
            print(f"REST backend not reachable.", file=sys.stderr)
        except requests.exceptions.Timeout:
            print(f"Request timed out.", file=sys.stderr)
        except requests.exceptions.MissingSchema:
            print(f"Error: Invalid URL.", file=sys.stderr)

    return None


def stat(args: Any) -> None:
    response = _fetch_data(
        args.backend,
        args.uuid,
        urljoin(args.base_url, f"file/{args.uuid}/stat/")
    )

    if response is not None:
        try:
            data = response.json()

            if args.output != "-":
                with open(args.output, "w") as dest_file:
                    print(f"File name: {data['name']}", file=dest_file)
                    print(f"Size: {data["size"]} bytes", file=dest_file)
                    print(f"MIME type: {data['mimetype']}", file=dest_file)
                    print(f"File created at: {data['create_datetime']}", file=dest_file)
            else:
                print(f"File name: {data['name']}")
                print(f"Size: {data["size"]} bytes")
                print(f"MIME type: {data['mimetype']}")
                print(f"File created at: {data['create_datetime']}")
        except ValueError:
            print(f"Error parsing JSON.", file=sys.stderr)
            sys.exit(1)

    else:
        sys.exit(1)


def read(args: Any) -> None:
    response = _fetch_data(
        args.backend,
        args.uuid,
        urljoin(args.base_url, f"file/{args.uuid}/read/")
    )

    if response is not None:
        data = response.content

        if args.output != "-":
            with open(args.output, "wb") as dest_file:
                dest_file.write(data)
        else:
            sys.stdout.buffer.write(data)

    else:
        sys.exit(1)


def main() -> None:
    parser = argparse.ArgumentParser(
        prog="file-client",
        description="A simple CLI application which retrieves and prints data from a REST API."
    )
    parser.add_argument(
        '-b',
        '--backend',
        choices=["grpc", "rest"],
        default="grpc",
        help='Set a backend to be used, choices are grpc and rest. Default is grpc.'
    )
    parser.add_argument(
        '-g',
        '--grpc-server',
        type=str,
        default="localhost:50051",
        help='Set a host and port of the gRPC server. Default is localhost:50051.'
    )
    parser.add_argument(
        '-u',
        '--base-url',
        type=str,
        default="http://localhost/",
        help='Set a base URL for a REST server. Default is http://localhost/.'
    )
    parser.add_argument(
        '-o',
        '--output',
        type=str,
        default="-",
        help='Set the file where to store the output. Default is -, i.e. the stdout.'
    )

    subparsers = parser.add_subparsers(
        title="subcommands", help="File operations"
    )

    parser_stat = subparsers.add_parser('stat', help='Prints the file metadata in a human-readable manner.')
    parser_stat.add_argument('uuid', help='UUID of the file')
    parser_stat.set_defaults(func=stat)

    parser_read = subparsers.add_parser('read', help='Outputs the file content.')
    parser_read.add_argument('uuid', help='UUID of the file')
    parser_read.set_defaults(func=read)

    args = parser.parse_args()

    if hasattr(args, "func"):
        args.func(args)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
