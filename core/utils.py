from sys import stderr
from os import getlogin
from socket import gethostname


__all__ = ["print_err", "ANSI_COLORS", "USERNAME", "HOSTNAME"]

ANSI_COLORS: dict[str, str] = {
    "RESET": "\033[0;0m",
    "RED": "\033[31m",
    "GREEN": "\033[32m",
    "YELLOW": "\033[33m",
}

USERNAME: str = getlogin()
HOSTNAME: str = gethostname()


def print_err(message: str) -> None:
    stderr.write(f"{message}\n")
