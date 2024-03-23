from zrb import Group

NOTO_GROUP = Group(name="noto", description="Noto management")
NOTO_WIKI_GROUP = Group(name="wiki", parent=NOTO_GROUP, description="Noto wiki")
