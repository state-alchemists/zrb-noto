from . import commit
from . import fetch
from . import pull
from . import push
from .local import check as local_check

assert commit
assert fetch
assert pull
assert push
assert local_check
