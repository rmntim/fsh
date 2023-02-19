import os
from core.utils import print_err


__all__ = ["change_directory", "exec_command"]


def exec_command(args: list[str]) -> None:
    os.execvp(args[1], args[1:])


def change_directory(args: list[str]) -> int:
    try:
        os.chdir(os.path.realpath(os.path.expanduser(args[1])))
        return 0
    except IndexError:
        os.chdir(os.environ["HOME"])
        return 0
    except NotADirectoryError:
        print_err("Not a directory!")
        return 1
    except PermissionError:
        print_err("Permission denied")
        return 1
