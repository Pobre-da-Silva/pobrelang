import logging
import sys
import time

from pobrelanglib import quotes

def is_token(candidate: str, token: str) -> bool:
    return candidate.startswith(token)

def parse_line(line: list[str]) -> None:
    if len(line) < 1:
        return

    match line[0]:
        case "WRK":
            if len(line) < 2:
                logging.error(quotes.lt_quote("not pass any parameters to the work keyword"))
                sys.exit()

            if len(line) > 2:
                logging.error(quotes.lt_quote("pass to many parameters to the work keyword"))
                sys.exit()

            if not is_token(line[1], "IDF"):
                logging.error(quotes.lt_quote("pass the wrong token to the work keyword"))
                sys.exit()

            try:
                work_hours = eval(line[1].split(":", 1)[1])

                if work_hours < 0:
                    raise
            except:
                logging.error(quotes.lt_quote("pass an invalid expression to the work keyword"))
                sys.exit()

            print(f"Working for {work_hours} h / {work_hours * 60} min / {work_hours * 60 * 60} sec.")
            time.sleep(work_hours * 60 * 60)

        case "SCR":
            if len(line) < 2:
                logging.error(quotes.lt_quote("not pass any parameters to the scream keyword"))
                sys.exit()

            if len(line) > 2:
                logging.error(quotes.lt_quote("pass to many parameters to the scream keyword"))
                sys.exit()

            if not is_token(line[1], "IDF"):
                logging.error(quotes.lt_quote("pass the wrong token to the scream keyword"))
                sys.exit()

            print(line[1].split(":", 1)[1])

        case _:
            logging.error(quotes.lt_quote("start an expression without a keyword"))
            sys.exit()
