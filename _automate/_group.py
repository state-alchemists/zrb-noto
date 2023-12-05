from zrb import Group
from .config import NOTO_GROUP_NAME

noto_group = Group(name=NOTO_GROUP_NAME)
noto_git_group = Group(name='git', parent=noto_group)
noto_git_local_group = Group(name='local', parent=noto_git_group)
noto_git_server_group = Group(name='server', parent=noto_git_group)
