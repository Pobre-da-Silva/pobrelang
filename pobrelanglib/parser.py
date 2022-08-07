import logging
import sys
import time

from pobrelanglib import quotes

variables: dict[str, str] = {}
money: float = 0.0

def is_token(candidate: str, token: str) -> bool:
    return candidate.startswith(token)

def extract_identifier(token: str) -> str:
    return token.split(":", 1)[1]

def parse_math(expression: str) -> str:
    operators = [
        "+", "-", "*", "/", "%", "=", "!", ">", "<", "&", "|", "^", "~"
    ]

    identifier: str = ""
    identifiers: list[str] = []

    for c in expression:
        if not c in operators:
            identifier += c
        else:
            if not identifier == "":
                try:
                    float(identifier)
                except:
                    identifiers.append(identifier)

                identifier = ""

    for id in identifiers:
        expression = expression.replace(id, variables[id])

    return str(eval(expression))

def parse_line(line: list[str]) -> None:
    global variables, money

    if len(line) < 1:
        return

    match line[0]:
        case "WRK":
            if len(line) < 2:
                logging.error(quotes.lt_quote("not pass any parameters to the work keyword"))
                sys.exit()

            if len(line) > 2:
                logging.error(quotes.lt_quote("pass too many parameters to the work keyword"))
                sys.exit()

            if not is_token(line[1], "EXP"):
                logging.error(quotes.lt_quote("pass the wrong token to the work keyword"))
                sys.exit()

            work_hours: float = 0.0

            try:
                if extract_identifier(line[1]) in variables:
                    work_hours = float(parse_math(variables[extract_identifier(line[1])]))
                else:
                    work_hours = float(parse_math(extract_identifier(line[1])))

                if work_hours < 0:
                    raise
            except:
                logging.error(quotes.lt_quote("pass an invalid expression to the work keyword"))
                sys.exit()

            print(f"Working for {work_hours} h / {work_hours * 60} min / {work_hours * 60 * 60} sec.")
            time.sleep(work_hours * 60 * 60)

            # 4 money per work hour
            money += work_hours * 4

            # taxes and monthly expenses
            money *= (100 - 96.1) / 100

            print(f"Current money: {money}.")

        case "SCR":
            if len(line) < 2:
                logging.error(quotes.lt_quote("not pass any parameters to the scream keyword"))
                sys.exit()

            for i in range(len(line)):
                if i == 0:
                    continue

                if not is_token(line[i], "EXP"):
                    logging.error(quotes.lt_quote("pass a wrong token to the scream keyword"))
                    sys.exit()

            for i in range(len(line)):
                if i == 0:
                    continue

                if extract_identifier(line[i]) in variables:
                    print(variables[extract_identifier(line[i])], end = "")
                else:
                    print(extract_identifier(line[i]), end = "")

                if not i == len(line) - 1:
                    print(" ", end = "")

            print()

        case "EXP":
            if not len(line) == 3 or not is_token(line[1], "EXP") and is_token(line[2], "EXP"):
                logging.error(quotes.lt_quote("create a variable like this"))
                sys.exit()

            if money - 0.0001 < 0:
                logging.error(quotes.lt_quote("try to create a variable with no money"))
                sys.exit()

            if not extract_identifier(line[1]).startswith("PobreLang/"):
                logging.error(quotes.rms_quote(extract_identifier(line[1])))
                sys.exit()

            try:
                variables[extract_identifier(line[1])] = pare_math(extract_identifier(line[2]))
            except:
                logging.error("try to create a variable with an invalid expression")
                sys.exit()

            money -= 0.0001

        case "TAG":
            if not len(line) == 3 or not is_token(line[1], "EXP") and is_token(line[2], "EXP"):
                logging.error(quotes.lt_quote("create a variable like this"))
                sys.exit()

            if money - 0.0001 < 0:
                logging.error(quotes.lt_quote("try to create a variable with no money"))
                sys.exit()

            if not extract_identifier(line[1]).startswith("PobreLang/"):
                logging.error(quotes.rms_quote(extract_identifier(line[1])))
                sys.exit()

            variables[extract_identifier(line[1])] = extract_identifier(line[2])
            money -= 0.0001

        case "NTE":
            pass

        case _:
            logging.error(quotes.lt_quote("start an expression without a keyword"))
            sys.exit()
