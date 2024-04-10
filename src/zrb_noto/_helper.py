import shutil


def get_screen_width() -> int:
    terminal_size = shutil.get_terminal_size()
    return terminal_size.columns
