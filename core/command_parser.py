__all__ = ["parse_commands"]


def parse_commands(command_str: str) -> list[str]:
    commands = (
        command_str.strip()
        .replace(";", " ; ")
        .replace(")", " ) ")
        .replace("(", " ( ")
        .replace("&&", " && ")
        .replace("||", " || ")
        .replace("\\", "")
        .split()
    )

    tokens = []
    subshell = []
    in_subshell = False
    s = ""

    for i, cmd in enumerate(commands):
        if cmd not in [";", "&&", "||", ")", "("]:
            s += cmd + " "
            if i == len(commands) - 1:
                tokens += [s.strip()] if s.strip() != "" else []
        elif cmd == "(":
            in_subshell = True
        else:
            if in_subshell:
                if cmd == ")":
                    subshell.append(s.strip())
                    tokens.append(subshell)
                    subshell = []
                    in_subshell = False
                else:
                    subshell.append(s.strip())
                    subshell.append(cmd)
            else:
                tokens += [s.strip()] if s.strip() != "" else []
                tokens.append(cmd)
            s = ""

    return tokens


def run_tests():
    # Single command
    assert parse_commands("ls") == ["ls"]

    # Single command with arguments
    assert parse_commands("cal -m") == ["cal -m"]

    # Multiple operators
    assert parse_commands("pwd&&ls; date") == ["pwd", "&&", "ls", ";", "date"]

    # Backslash continuation
    assert parse_commands("ls \\-la") == ["ls -la"]

    # Bad backslash usage
    assert parse_commands("cal\\-m") == ["cal-m"]

    # Subshells
    assert parse_commands("(cd /tmp && pwd); pwd") == [
        ["cd /tmp", "&&", "pwd"],
        ";",
        "pwd",
    ]


if __name__ == "__main__":
    print(parse_commands("(cd /tmp && pwd); pwd"))
    run_tests()
    print("All test passed!")
