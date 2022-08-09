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
file_content: list[str] = []

try:
    with open(filename) as file:
        while line := file.readline():
            file_content.append(line)
except IOError:
    logging.error(quotes.lt_quote("pass an unexisting file to the interpreter"))
    sys.exit()

del filename

def iterate_file_content(activity) -> None:
    while not parser.line_number == len(file_content):
        parser.line_number += 1
        activity()

def process_stamps() -> None:
    line = file_content[parser.line_number - 1]

    line_tokens = lexer.lex_line(line)

    if len(line_tokens) > 0 and parser.is_token(line_tokens[0], "STM"):
        parser.parse_line(line_tokens)

def parse_linearly() -> None:
    parser.parse_line(lexer.lex_line(file_content[parser.line_number - 1]))

iterate_file_content(process_stamps)
del process_stamps
parser.line_number = 0
iterate_file_content(parse_linearly)
