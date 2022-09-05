#!/usr/bin/python3

import logging
import os
import sys

from pobrelanglib import quotes

if not __name__ == "__main__":
    logging.error(quotes.lt_quote("run PobreLang as a library"))
    sys.exit()

if not len(sys.argv) == 2:
    logging.error(quotes.lt_quote("not specify a filename to the interpreter"))
    sys.exit()

from pobrelanglib import lexer, pl_parser, module as modlib
from pobrelanglib.module import Module

main_module: Module = Module("main", os.path.abspath(sys.argv[1]))

if not main_module.open_file():
    logging.error(quotes.lt_quote("pass an unexisting file to the interpreter"))
    sys.exit()

modlib.set_main_module(main_module)

def parse_linearly(module: Module) -> None:
    pl_parser.parse_line(lexer.lex_line(module.file_content[module.line_number -1]), module)

modlib.main_module.line_number = 0
modlib.current_module = modlib.main_module

def parse():
    while True:
        module = modlib.current_module
        module.line_number += 1
        parse_linearly(module)
        
        if module.line_number == len(module.file_content):
            if module == modlib.main_module:
                sys.exit()
            logging.error(quotes.lt_quote("use a module with a stamp that holds the execution"))
            sys.exit()    

parse()
