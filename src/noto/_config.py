import os
from datetime import datetime

_HOME_DIR = os.path.expanduser("~")
_SYSTEM_USER = os.getenv("USER", "incognito")
_DEFAULT_REMOTE_GIT_URL = f"git@github.com:{_SYSTEM_USER}/daily.git"

REMOTE_GIT_URL = os.getenv("NOTO_REMOTE_GIT", _DEFAULT_REMOTE_GIT_URL)
LOCAL_REPO_DIR = os.path.abspath(os.getenv("NOTO_LOCAL_REPO", f"{_HOME_DIR}/daily"))
TODO_FILE_PATH = os.getenv("NOTO_TODO_FILE", "todo.txt")
DONE_FILE_PATH = os.getenv("NOTO_DONE_FILE", "done.txt")
WIKI_DIR_PATH = os.getenv("NOTO_WIKI_DIR", "wiki")
LOG_DIR_PATH = os.getenv("NOTO_LOG_DIR", "log")

TODO_ABS_FILE_PATH = os.path.abspath(os.path.join(LOCAL_REPO_DIR, TODO_FILE_PATH))
DONE_ABS_FILE_PATH = os.path.abspath(os.path.join(LOCAL_REPO_DIR, DONE_FILE_PATH))
WIKI_ABS_DIR_PATH = os.path.abspath(os.path.join(LOCAL_REPO_DIR, WIKI_DIR_PATH))
LOG_ABS_DIR_PATH = os.path.abspath(os.path.join(LOCAL_REPO_DIR, LOG_DIR_PATH))

CURRENT_TIME = datetime.now()
CURRENT_YEAR = CURRENT_TIME.year
CURRENT_MONTH = CURRENT_TIME.strftime("%m")
CURRENT_DAY = CURRENT_TIME.strftime("%d")
