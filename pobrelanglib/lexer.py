def lex_line(line: str) -> list[str]:
    line = line.replace("\n", "")
    token_candidates = line.split(" ")
    tokens: list[str] = []

    for candidate in token_candidates:
        match candidate:
            case "scream":
                tokens.append("SCR")

            case "work":
                tokens.append("WRK")

            case "item":
                tokens.append("ITM")

            case "tag":
                tokens.append("TAG")

            case "note":
                tokens.append("NTE")

            case _:
                tokens.append("IDF:" + candidate)

    return tokens
