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

            if not is_token(line[1], "IDF"):
                logging.error(quotes.lt_quote("pass the wrong token to the work keyword"))
                sys.exit()

            work_hours: float = 0.0

            try:
                if extract_identifier(line[1]) in variables:
                    work_hours = eval(variables[extract_identifier(line[1])])
                else:
                    work_hours = eval(extract_identifier(line[1]))

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

                if not is_token(line[i], "IDF"):
                    logging.error(quotes.lt_quote("pass the wrong token to the scream keyword"))
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

        case "ITM":
            if not len(line) == 3 or not is_token(line[1], "IDF") and is_token(line[2], "IDF"):
                logging.error(quotes.lt_quote("create a variable like this"))
                sys.exit()

            if money - 0.0001 < 0:
                logging.error(quotes.lt_quote("try to create a variable with no money"))
                sys.exit()

            variables[extract_identifier(line[1])] = extract_identifier(line[2])
            money -= 0.0001

        case _:
            logging.error(quotes.lt_quote("start an expression without a keyword"))
            sys.exit()
