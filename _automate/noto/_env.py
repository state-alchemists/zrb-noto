from zrb import Env

from _automate._exim._config import PROJECT_DIR

PROJECT_DIR_ENV = Env(name="PROJECT_DIR", default=PROJECT_DIR, os_name="")
