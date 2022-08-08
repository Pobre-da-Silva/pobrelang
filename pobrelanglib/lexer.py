def lex_line(line: str) -> list[str]:
    line = line.replace("\n", "").replace("\t", "")
    token_candidates = line.split(" ")
    del line
    tokens: list[str] = []

    for candidate in token_candidates:
        match candidate:
            case "scream":
                tokens.append("SCR")

            case "listen":
                tokens.append("LST")

            case "antidisestablishmentarianism":
                tokens.append("ADM")

            case "work":
                tokens.append("WRK")

            case "item":
                tokens.append("ITM")

            case "tag":
                tokens.append("TAG")

            case "stamp":
                tokens.append("STM")

            case "sprint":
                tokens.append("SPR")

            case "if":
                tokens.append("IFS")

            case "burn":
                tokens.append("BRN")

            case "note":
                tokens.append("NTE")

            case _:
                if not candidate == "":
                    tokens.append("EXP:" + candidate)

    del token_candidates

    return tokens
