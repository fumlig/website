#!/usr/bin/env python3

import argparse

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


if __name__ == "__main__":
    main()