#!/usr/bin/env python3

import os
import argparse
import threading
import http.server

import pyinotify

import generator


def main():
    parser = argparse.ArgumentParser(description="Generate static website.")
    parser.add_argument("path", help="Website path.")
    parser.add_argument("-c", "--content-path", help="Content path")
    parser.add_argument("-g", "--generated-path", help="Generated path")
    parser.add_argument("-s", "--static-path", help="Static path")
    parser.add_argument("-t", "--templates-path", help="Templates path")


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


def init_website(args, drafts=False):
    return generator.Website(
        path=args.path,
        content_path=args.content_path,
        generated_path=args.generated_path,
        static_path=args.static_path,
        templates_path=args.templates_path,
        drafts_enabled=drafts
    )


def create(args):
    print("Creating website '{}'".format(args.path))
    website = init_website(args)
    website.create()


def generate(args):
    """Generate website with drafts disabled."""
    print("Generating website '{}'".format(args.path))
    website = init_website(args)
    website.generate()


def serve(args):
    """
    Serve website on localhost with drafts enabled.
    Watch for changes and automatically generate.
    """
    website = init_website(args, drafts=True)
    # watch for changes
    watch_thread = threading.Thread(target=watch_website, args=(website,))
    watch_thread.start()
    # start server
    serve_thread = threading.Thread(target=serve_website, args=(website, args.port))
    serve_thread.start()


def watch_website(website):
    """Watch website for changes and generate when they happen."""
    print("Watching website '{}'".format(website.path))
    
    wm = pyinotify.WatchManager()
    mask = pyinotify.IN_CREATE | pyinotify.IN_DELETE | pyinotify.IN_MODIFY
    
    class EventHandler(pyinotify.ProcessEvent):
        def process_IN_CREATE(self, event):
            print("{} created, generating".format(event.pathname))
            website.generate()
        def process_IN_DELETE(self, event):
            print("{} deleted, generating".format(event.pathname))
            website.generate()
        def process_IN_MODIFY(self, event):
            print("{} modified, generating".format(event.pathname))
            website.generate()
    
    handler = EventHandler()
    notifier = pyinotify.Notifier(wm, handler)

    wdd = wm.add_watch(website.content_path, mask, rec=True)
    wdd = wm.add_watch(website.static_path, mask, rec=True)
    wdd = wm.add_watch(website.templates_path, mask, rec=True)
    notifier.loop()


def serve_website(website, port):
    """Serve website."""
    print("Serving website '{}' on {}".format(website.path, port))
    
    server_address = ("", port)

    class RequestHandler(http.server.SimpleHTTPRequestHandler):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, directory=website.generated_path, **kwargs)

    httpd = http.server.HTTPServer(server_address, RequestHandler)
    httpd.serve_forever()


if __name__ == "__main__":
    main()