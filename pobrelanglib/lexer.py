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

            case _:
                tokens.append("IDF:" + candidate)

    return tokens
