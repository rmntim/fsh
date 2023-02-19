import os
import sys
from core.utils import print_err, ANSI_COLORS, HOSTNAME, USERNAME
from core.command_parser import parse_commands
from core.fsh_builtins import change_directory, exec_command


def run_command(args: list[str]) -> int:
    command: str = args[1] if args[0] == "!" else args[0]
    pid: int = os.fork()
    if pid == 0:
        os.execvp(command, args)
    _, exit_status = os.waitpid(pid, 0)
    return exit_status


def generate_prompt(exit_status: int) -> str:
    curr_dir: str = os.getcwd().split("/")[-1]
    curr_dir = curr_dir if curr_dir != USERNAME else "~"
    if exit_status == 0:
        return f"[{USERNAME}@{HOSTNAME} {curr_dir}]$ "
    else:
        return f"[{USERNAME}@{HOSTNAME} {curr_dir}]{ANSI_COLORS['RED']}${ANSI_COLORS['RESET']} "  # noqa E501


def main() -> None:

    exit_status = 0

    while True:
        try:
            sys.stdout.write(f"{generate_prompt(exit_status)}")
            sys.stdout.flush()
            commands = parse_commands()
            if len(commands) == 0:
                sys.stdout.write("\n")
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
                        match args[0]:
                            case "exit":
                                sys.exit()
                            case "exec":
                                exec_command(args)
                            case "cd":
                                exit_status = change_directory(args)
                            case "!":
                                exit_status = int(not run_command(args))
                            case _:
                                exit_status = run_command(args)
        except FileNotFoundError:
            print_err("No such file or directory")
            exit_status = 1
        except KeyboardInterrupt:
            sys.stdout.write("\n")
            continue


if __name__ == "__main__":
    main()
