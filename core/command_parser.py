import sys

__all__ = ["parse_commands"]


def parse_commands() -> list[str]:
    stdinput = (
        sys.stdin.readline()
        .replace(";", " ; ")
        .replace("&&", " && ")
        .replace("||", " || ")
        .split()
    )

    commands = []
    s = ""
    for i in range(len(stdinput)):
        if stdinput[i] not in [";", "&&", "||"]:
            s += stdinput[i] + " "
            if i == len(stdinput) - 1:
                commands.append(s.strip())
        else:
            commands.append(s.strip())
            commands.append(stdinput[i])
            s = ""

    return commands
