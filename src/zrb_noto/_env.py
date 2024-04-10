from zrb import Env

from ._config import LOCAL_REPO_DIR, REMOTE_GIT_URL

REMOTE_GIT_URL_ENV = Env(name="REMOTE_GIT_URL", os_name="", default=REMOTE_GIT_URL)
LOCAL_REPO_DIR_ENV = Env(name="LOCAL_REPO_DIR", os_name="", default=LOCAL_REPO_DIR)
