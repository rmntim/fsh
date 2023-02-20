__all__ = ["parse_commands"]


def parse_commands(command_str: str) -> list[str]:
    commands = (
        command_str.strip()
        .replace(";", " ; ")
        .replace("&&", " && ")
        .replace("||", " || ")
        .replace("\\", "")
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


if __name__ == "__main__":
    run_tests()
    print("All test passed!")
