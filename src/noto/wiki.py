import os
from typing import List

from zrb import Task, create_wiki_tasks, runner

from ._config import WIKI_ABS_DIR_PATH
from ._group import noto_wiki_group


wiki_tasks: List[Task] = []
if os.path.isdir(WIKI_ABS_DIR_PATH):
    wiki_tasks = create_wiki_tasks(
        directory=WIKI_ABS_DIR_PATH, group=noto_wiki_group, runner=runner
    )
