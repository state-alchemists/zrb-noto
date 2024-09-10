import os
from datetime import datetime

from zrb.helper.string.conversion import to_boolean

_HOME_DIR = os.path.expanduser("~")
_SYSTEM_USER = os.getenv("USER", "incognito")
_DEFAULT_REMOTE_GIT_URL = f"git@github.com:{_SYSTEM_USER}/daily.git"

IS_AUTO_SYNC = to_boolean(os.getenv("NOTO_AUTO_SYNC", "true"))
REMOTE_GIT_URL = os.getenv("NOTO_REMOTE_GIT", _DEFAULT_REMOTE_GIT_URL)
LOCAL_REPO_DIR = os.path.abspath(os.getenv("NOTO_LOCAL_REPO", f"{_HOME_DIR}/daily"))
TODO_FILE_PATH = os.getenv("NOTO_TODO_FILE", "todo.txt")
NOTE_FILE_PATH = os.getenv("NOTO_NOTE_FILE", "note.md")
DONE_FILE_PATH = os.getenv("NOTO_DONE_FILE", "done.txt")
WIKI_DIR_PATH = os.getenv("NOTO_WIKI_DIR", "wiki")
LOG_DIR_PATH = os.getenv("NOTO_LOG_DIR", "log")

TODO_ABS_FILE_PATH = os.path.abspath(os.path.join(LOCAL_REPO_DIR, TODO_FILE_PATH))
NOTE_ABS_FILE_PATH = os.path.abspath(os.path.join(LOCAL_REPO_DIR, NOTE_FILE_PATH))
DONE_ABS_FILE_PATH = os.path.abspath(os.path.join(LOCAL_REPO_DIR, DONE_FILE_PATH))
WIKI_ABS_DIR_PATH = os.path.abspath(os.path.join(LOCAL_REPO_DIR, WIKI_DIR_PATH))
LOG_ABS_DIR_PATH = os.path.abspath(os.path.join(LOCAL_REPO_DIR, LOG_DIR_PATH))

CURRENT_TIME = datetime.now()
CURRENT_YEAR = CURRENT_TIME.year
CURRENT_MONTH = CURRENT_TIME.strftime("%m")
CURRENT_DAY = CURRENT_TIME.strftime("%d")
