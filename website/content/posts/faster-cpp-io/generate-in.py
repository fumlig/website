#!/usr/bin/env python3

import os
import random


FILE = os.path.join(os.path.dirname(__file__), "in.txt")

if __name__ == "__main__":
    with open(FILE, 'w') as f:
        for d in range(1000000):
            f.write("{} ".format(random.randint(-10000, 10000)))