__all__ = ["parse_commands"]


def parse_commands(command_str: str) -> list[str]:
    commands = (
        command_str.strip()
        .replace(";", " ; ")
        .replace("&&", " && ")
        .replace("||", " || ")
        .split()
    )

    tokens = []
    s = ""
    for i in range(len(commands)):
        if commands[i] not in [";", "&&", "||"]:
            s += commands[i] + " "
            if i == len(commands) - 1:
                tokens.append(s.strip())
        else:
            tokens.append(s.strip())
            tokens.append(commands[i])
            s = ""

    return tokens
