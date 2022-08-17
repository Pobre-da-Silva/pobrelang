import logging
import sys
import time

from pobrelanglib import quotes
from pobrelanglib.module import Module
from pobrelanglib import module as modlib

money: float = 0.0
variable_cost: float = 0.0001

callstack: list[tuple[Module, int]] = []

def lt_panic(idea: str) -> None:
    logging.error(quotes.lt_quote(idea))
    sys.exit()

def is_token(candidate: str, token: str) -> bool:
    return candidate.startswith(token)

def extract_expression(token: str) -> str:
    return token.split(":", 1)[1]

def parse_math(expr: str, module: Module) -> str:
    for var, val in module.variables.items():
        expr = expr.replace(var, val)

    return str(float(eval(expr)))

def create_variable(type: str, name: str, value: str, module: Module) -> None:
    global money

    if not name.startswith("PobreLang/"):
        logging.error(quotes.rms_quote(name))
        sys.exit()

    if not name in module.variables:
        try:
            assert money - variable_cost > 0
        except AssertionError:
            lt_panic("try to create a variable with no money")

        money -= variable_cost

    match type:
        case "ITM":
            try:
                module.variables[name] = parse_math(value, module)
            except (NameError, SyntaxError):
                lt_panic("try to create a variable with an invalid expression")

        case "TAG":
            module.variables[name] = value

def goto(module: Module, line: list[str], use_callstack: bool = False) -> None:
    if not len(line) == 2 or not is_token(line[1], "EXP"):
        lt_panic("try to sprint not knowing where to")

    stamp = extract_expression(line[1])
    stm_mod = None

    for mod in modlib.included_modules:
        for st in mod.stamps:
            #print(stamp +" -> " + st)
            if st == stamp:
                stm_mod = mod
                break

    if stm_mod == None:
        lt_panic("sprint to a non-existing stamp")

    modlib.current_module = stm_mod
    stm_mod.line_number = stm_mod.stamps[stamp]
    
    if use_callstack: callstack.append((module, module.line_number))

def parse_line(line: list[str], module: Module) -> None:
    global money

    # empty line
    if len(line) < 1:
        return

    match line[0]:
        case "INC":
            if len(line) < 2:
                lt_panic("not learn to include libraries")
            
            if not modlib.include_module(extract_expression(line[1])):
                lt_panic("include a module that does not exists")

        case "WRK":
            try:
                assert len(line) == 2
            except AssertionError:
                lt_panic("pass a wrong number of arguments to the work keyword")

            work_hours: float = 0.0

            try:
                expr = extract_expression(line[1])

                if expr in module.variables:
                    work_hours = float(parse_math(module.variables[expr], module))
                else:
                    work_hours = float(parse_math(expr, module))

                del expr

                assert work_hours > 0
            except (IndexError, NameError, SyntaxError, AssertionError):
                lt_panic("pass an invalid expression to the work keyword")

            work_mins = work_hours * 60
            work_secs = work_mins * 60
            print(f"Working for {work_hours} h / {work_mins} min / {work_secs} sec.")
            del work_mins
            time.sleep(work_secs)
            del work_secs

            # 4 money per work hour
            money += work_hours * 4

            del work_hours

            # taxes and monthly expenses
            money *= (100 - 96.1) / 100

            print(f"Work done! Current money: {money}.")

        case "SCR":
            if len(line) < 2:
                lt_panic("not pass any parameters to the scream keyword")

            for i in range(len(line)):
                # ignore first arg, which is the keyword
                if i == 0:
                    continue

                if not is_token(line[i], "EXP"):
                    lt_panic("pass a wrong token to the scream keyword")

            for i in range(len(line)):
                # ignore first arg, which is the keyword
                if i == 0:
                    continue

                expr = extract_expression(line[i])

                if expr in module.variables:
                    print(module.variables[expr], end = "")
                else:
                    print(extract_expression(line[i]), end = "")

                del expr

                print(" ", end = "")

            # just a line break
            print()

        case "LST" | "ADM":
            if not len(line) == 2 or not is_token(line[1], "EXP"):
                lt_panic("not learn how to use the input keywords correctly")

            var = extract_expression(line[1])

            if not var in module.variables:
                lt_panic("read user input into a non-existing variable")

            match line[0]:
                case "LST":
                    module.variables[var] = input()
                case "ADM":
                    try:
                        module.variables[var] = parse_math(input(), module)
                    except (NameError, SyntaxError):
                        lt_panic("input an invalid expression to the parser")

        case "ITM" | "TAG":
            if not len(line) == 3 or not (is_token(line[1], "EXP") and is_token(line[2], "EXP")):
                lt_panic("create a variable like this")

            create_variable(line[0], extract_expression(line[1]), extract_expression(line[2]), module)

        case "STM":
            if not len(line) == 2 or not is_token(line[1], "EXP"):
                lt_panic("create a stamp in this stupid way")

            name = extract_expression(line[1])

            if not name.startswith("PobreLang/"):
                logging.error(quotes.rms_quote(name))
                sys.exit()

            module.stamps[name] = module.line_number

        case "SPR":
            goto(module, line)
        
        case "DSP":
            goto(module, line, True)

        case "GBK":
            if len(callstack) > 0:
                item = callstack.pop()
                mod = item[0]
                mod.line_number = item[1]
                modlib.current_module = mod

        case "IFS":
            if not len(line) == 3 or not (is_token(line[1], "EXP") and is_token(line[2], "EXP")):
                lt_panic("create an if statement with this structure")

            condition = extract_expression(line[1])
            stamp = extract_expression(line[2])

            if not stamp in module.stamps:
                lt_panic("not pass a valid stamp to an if statement")

            condition_result = 0

            try:
                condition_result = bool(float(parse_math(condition, module = module)))
            except (NameError, SyntaxError):
                lt_panic("pass an invalid expression to an if statement")

            del condition

            if condition_result == True:
                module.last_line = module.line_number
                module.line_number = module.stamps[stamp]

        case "BRN":
            if not len(line) == 2 or not is_token(line[1], "EXP"):
                lt_panic("try to delete a variable without knowing how to use the burn keyword")

            try:
                module.variables.pop(extract_expression(line[1]))
            except KeyError:
                lt_panic("try to delete a variable that does not exist")

        case "NTE":
            pass

        case _:
            lt_panic("start an expression without a keyword")
