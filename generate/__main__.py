#!/usr/bin/env python3

import argparse
import generate


def main():
    parser = argparse.ArgumentParser(description="Generate static website.")
    parser.add_argument("dir", help="Website directory.")
    
    args = parser.parse_args()

    generate.generate(args.dir)


if __name__ == "__main__":
    main()