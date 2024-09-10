import os
import shutil


def get_screen_width() -> int:
    terminal_size = shutil.get_terminal_size()
    return terminal_size.columns


def get_note_content(note_path: str) -> str:
    if not os.path.isfile(note_path):
        return ""
    with open(note_path, "r") as f:
        return f.read()
