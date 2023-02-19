import sys


__all__ = ["print_err"]


def print_err(message: str) -> None:
    sys.stderr.write(f"{message}\n")
