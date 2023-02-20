import os
import sys
from core.utils import print_err, ANSI_COLORS, HOSTNAME, USERNAME
from core.command_parser import parse_commands
from core.fsh_builtins import change_directory, exec_command


def run_command(args: list[str]) -> int:
    command: str = args[0]
    exit_status: int = 0
    match command:
        case "exit":
            sys.exit()
        case "exec":
            exec_command(args[1:])
        case "cd":
            exit_status = change_directory(args)
        case "!":
            exit_status = int(not run_command(args[1:]))
        case _:
            pid: int = os.fork()
            if pid == 0:
                try:
                    os.execvp(command, args)
                except FileNotFoundError:
                    print_err("File not found")
                    sys.exit(1)
            else:
                _, exit_status = os.waitpid(pid, 0)
    return exit_status


def generate_prompt(exit_status: int) -> str:
    curr_dir: str = os.getcwd().split("/")[-1]
    curr_dir = curr_dir if curr_dir != USERNAME else "~"
    if exit_status == 0:
        return f"[{USERNAME}@{HOSTNAME} {curr_dir}]$ "
    else:
        return f"[{USERNAME}@{HOSTNAME} {curr_dir}]{ANSI_COLORS['RED']}${ANSI_COLORS['RESET']} "  # noqa E501


def read_line() -> str:
    result: str = ""
    line: str = sys.stdin.readline()
    if len(line) < 1 or len(line) == 1 and line[0] == "\n":
        return line
    while str.encode(line)[-2] == 92:
        sys.stdout.write("... > ")
        sys.stdout.flush()
        result += line.replace("\\", "").strip()
        line = sys.stdin.readline()

    result += " " + line
    return result


def main() -> None:

    exit_status = 0

    while True:
        try:
            sys.stdout.write(f"{generate_prompt(exit_status)}")
            sys.stdout.flush()
            command_str = read_line()

            commands: list[str] = parse_commands(command_str)
            if len(commands) == 0:
                match str.encode(command_str):
                    case b"":
                        print("\nexit")
                        sys.exit()
                    case b"\n":
                        continue
            for command in commands:
                match command:
                    case ";":
                        continue
                    case "&&":
                        if exit_status == 0:
                            continue
                        else:
                            break
                    case "||":
                        if exit_status != 0:
                            continue
                        else:
                            break
                    case cmd:
                        args = cmd.split()
                        exit_status = run_command(args)
        except KeyboardInterrupt:
            sys.stdout.write("\n")


if __name__ == "__main__":
    main()
