#!/usr/bin/env python3

import os
import argparse
import http.server

import generator


def main():
    parser = argparse.ArgumentParser(description="Generate static website.")
    parser.add_argument("path", help="Website path.")

    subparsers = parser.add_subparsers()

    # create
    parser_create = subparsers.add_parser("create", help="Create website.")
    parser_create.set_defaults(func=create)

    # generate
    parser_generate = subparsers.add_parser("generate", help="Generate website.")
    parser_generate.set_defaults(func=generate)

    # serve
    parser_serve = subparsers.add_parser("serve", help="Serve website.")
    parser_serve.add_argument("-p", "--port", type=int, default=8080, help="Port to serve website on.")
    parser_serve.set_defaults(func=serve)

    args = parser.parse_args()
    args.func(args)


def create(args):
    print("Creating website " + args.path)
    website = generator.Website(args.path, generator.Config())
    website.create()


def generate(args):
    print("Generating website " + args.path)
    website = generator.Website(args.path, generator.Config())
    website.generate()


def serve(args):
    print("Serving website on " + str(args.port))
    website = generator.Website(args.path, generator.Config())
    os.chdir(website.generated_path)
    server_address = ("", args.port)
    httpd = http.server.HTTPServer(server_address, http.server.SimpleHTTPRequestHandler)
    httpd.serve_forever()


if __name__ == "__main__":
    main()