import logging
import sys
import time

from pobrelanglib import quotes

variables: dict[str, str] = {}
money: float = 0.0
variable_cost: float = 0.0001
line_number: int = 0
stamps: dict[str, int] = {}

def lt_panic(idea: str) -> None:
    logging.error(quotes.lt_quote(idea))
    sys.exit()

def is_token(candidate: str, token: str) -> bool:
    return candidate.startswith(token)

def extract_expression(token: str) -> str:
    return token.split(":", 1)[1]

def parse_math(expr: str) -> str:
    for var, val in variables.items():
        expr = expr.replace(var, val)

    return str(float(eval(expr)))

def create_variable(type: str, name: str, value: str) -> None:
    global variables, money

    if not name.startswith("PobreLang/"):
        logging.error(quotes.rms_quote(name))
        sys.exit()

    if not name in variables:
        try:
            assert money - variable_cost > 0
        except AssertionError:
            lt_panic("try to create a variable with no money")

        money -= variable_cost

    match type:
        case "ITM":
            try:
                variables[name] = parse_math(value)
            except (NameError, SyntaxError):
                lt_panic("try to create a variable with an invalid expression")

        case "TAG":
            variables[name] = value

def parse_line(line: list[str]) -> None:
    global money, variables, stamps, line_number

    # empty line
    if len(line) < 1:
        return

    match line[0]:
        case "WRK":
            try:
                assert len(line) == 2
            except AssertionError:
                lt_panic("pass a wrong number of arguments to the work keyword")

            work_hours: float = 0.0

            try:
                expr = extract_expression(line[1])

                if expr in variables:
                    work_hours = float(parse_math(variables[expr]))
                else:
                    work_hours = float(parse_math(expr))

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

                if expr in variables:
                    print(variables[expr], end = "")
                else:
                    print(extract_expression(line[i]), end = "")

                del expr

                print(" ", end = "")

            # just a line break
            print()

        case "ITM" | "TAG":
            if not len(line) == 3 or not (is_token(line[1], "EXP") and is_token(line[2], "EXP")):
                lt_panic("create a variable like this")

            create_variable(line[0], extract_expression(line[1]), extract_expression(line[2]))

        case "STM":
            if not len(line) == 2 or not is_token(line[1], "EXP"):
                lt_panic("create a stamp in this stupid way")

            name = extract_expression(line[1])

            if not name.startswith("PobreLang/"):
                logging.error(quotes.rms_quote(name))
                sys.exit()

            if not name in stamps:
                try:
                    assert money - variable_cost > 0
                except AssertionError:
                    lt_panic("try to create a stamp with no money")

                money -= variable_cost

            stamps[name] = line_number

        case "SPR":
            if not len(line) == 2 or not is_token(line[1], "EXP"):
                lt_panic("try to sprint not knowing where to")

            stamp = extract_expression(line[1])

            if not stamp in stamps:
                lt_panic("sprint to a non-existing stamp")

            line_number = stamps[stamp]

        case "IFS":
            if not len(line) == 3 or not (is_token(line[1], "EXP") and is_token(line[2], "EXP")):
                lt_panic("create an if statement with this structure")

            condition = extract_expression(line[1])
            stamp = extract_expression(line[2])

            if not stamp in stamps:
                lt_panic("not pass a valid stamp to an if statement")

            condition_result = 0

            try:
                condition_result = bool(float(parse_math(condition)))
            except (NameError, SyntaxError):
                lt_panic("pass an invalid expression to an if statement")

            del condition

            if condition_result == True:
                line_number = stamps[stamp]

        case "BRN":
            if not len(line) == 2 or not is_token(line[1], "EXP"):
                lt_panic("try to delete a variable without knowing how to use the burn keyword")

            try:
                variables.pop(extract_expression(line[1]))
            except KeyError:
                lt_panic("try to delete a variable that does not exist")

        case "NTE":
            pass

        case _:
            lt_panic("start an expression without a keyword")
