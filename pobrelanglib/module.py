from os import path, getcwd

from pobrelanglib import lexer, pl_parser

class Module:
    name: str = None
    file_name: str = None
    file_content: list[str] = []

    variables: dict[str, str] = {}
    line_number: int = 0
    stamps: dict[str, int] = {}

    def __init__(self, name, file_name):
        self.name = name
        self.file_name = file_name
  
    def open_file(self) -> bool:
        if self.file_content == None:
            return False
    
        file_content: list[str] = []

        try:
            with open(self.file_name) as file:
                while line := file.readline():
                    file_content.append(line)
            
            self.file_content = file_content
            return True
        except IOError:
            return False


main_module: Module = None
current_module: Module = None
included_modules: list[Module] = []

def parse_module_file_name(name: str) -> str:
    return path.join(getcwd(), f"{name}.pbr")

def process_stamps(module: Module) -> None:
    line = module.file_content[module.line_number -1]

    line_tokens = lexer.lex_line(line)

    if len(line_tokens) > 0 and pl_parser.is_token(line_tokens[0], "STM"):
        pl_parser.parse_line(line_tokens, module)

def set_main_module(module: Module) -> None:
    global main_module
    main_module = module
    iterate_file_content(main_module, process_stamps)
    included_modules.append(main_module)

def include_module(module_name: str) -> bool:
    for mod in included_modules:
        if mod.name == module_name: return True
    
    module = Module(module_name, parse_module_file_name(module_name))

    if not module.open_file(): return False

    iterate_file_content(module, process_stamps)
    included_modules.append(module)
    return True

def iterate_file_content(module, activity) -> None:
    while not module.line_number == len(module.file_content):
        module.line_number += 1
        activity(module)
