import os
from datetime import datetime

CURRENT_DIR = os.path.dirname(__file__)
PROJECT_DIR = os.path.dirname(os.path.dirname(CURRENT_DIR))
SRC_DIR = os.path.join(PROJECT_DIR, "src")
TODO_FILE_NAME = os.path.join(SRC_DIR, "todo.txt")

CURRENT_TIME = datetime.now()
