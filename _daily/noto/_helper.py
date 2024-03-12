import os
import shutil
import subprocess

from zrb import Task
from zrb.helper.accessories.color import colored


def sync_noto(task: Task) -> int:
    current_dir = os.path.dirname(__file__)
    try:
        return run_cmd_path(task, os.path.join(current_dir, "sync.sh"))
    except Exception:
        task.print_err(colored("Cannot sync", color="light_red"))
        return 0


def run_cmd_path(task: Task, command_path: str) -> int:
    with open(command_path, "r") as file:
        command = file.read()
        return run_cmd(task, command)


def run_cmd(task: Task, command: str) -> int:
    # Start the process
    process = subprocess.Popen(
        command,
        shell=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        env=task.get_env_map(),
    )
    # Iterate over the output lines as they become available
    while True:
        output = process.stdout.readline()
        if output == "" and process.poll() is not None:
            break
        if output:
            task.print_out_dark(output.strip())
    rc = process.poll()
    if rc != 0:
        raise Exception(f"Non zero exit code: {rc}")
    return rc


def get_screen_width() -> int:
    terminal_size = shutil.get_terminal_size()
    return terminal_size.columns
