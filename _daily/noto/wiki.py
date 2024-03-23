import os
from zrb import create_wiki_tasks, runner

from _daily.noto._config import SRC_DIR
from _daily.noto._group import NOTO_WIKI_GROUP

wiki_dir = os.path.join(SRC_DIR, "wiki")

if os.path.isdir(wiki_dir):
    create_wiki_tasks(directory=wiki_dir, group=NOTO_WIKI_GROUP, runner=runner)
