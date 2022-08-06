#!/usr/bin/python3

import logging
import sys

from pobrelanglib import quotes

if not __name__ == "__main__":
    logging.error(quotes.lt_quote("run PobreLang as a library"))
    sys.exit()

if not len(sys.argv) == 2:
    logging.error(quotes.lt_quote("not specify a filename to the interpreter"))
    sys.exit()

from pobrelanglib import lexer, parser

filename = sys.argv[1]
raw_code: str

try:
    with open(filename) as file:
        while line := file.readline():
            parser.parse_line(lexer.lex_line(line))
except IOError:
    logging.error(quotes.lt_quote("pass an unexisting file to the interpreter"))
    sys.exit()
