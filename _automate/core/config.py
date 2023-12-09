from zrb.helper.string.conversion import to_boolean
import os

NOTO_GROUP_NAME = os.getenv('NOTO_GROUP_NAME', 'noto')
NOTO_GIT_REMOTE_NAME = os.getenv('NOTO_GIT_REMOTE_NAME', 'origin')
NOTO_MACHINE_NAME = os.getenv('NOTO_MACHINE_NAME', 'local')
NOTO_USE_FALLBACK = to_boolean(os.getenv('NOTO_USE_FALLBACK', '0'))
