#!/usr/bin/python3

import logging
import sys

if not __name__ == "__main__":
    logging.error("PobreLang is NOT a library and should not be run as such!");
    sys.exit()

if not len(sys.argv) == 2:
    logging.error("Incorrect number of arguments! Please specify a filename!");
    sys.exit()

filename = sys.argv[1]
raw_code: str

try:
    with open(filename) as file:
        while line := file.readline():
            print(line)
except:
    logging.error("File not found!")
    sys.exit()
