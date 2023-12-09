from _automate.core.config import NOTO_USE_FALLBACK
import os
import shutil
import sys
import traceback

CURRENT_DIR = os.path.dirname(__file__)
FALLBACK_PATH = os.path.join(CURRENT_DIR, '_automate', 'fallback.py')

if NOTO_USE_FALLBACK:
    print('🤖 Load _automate.fallback', file=sys.stderr)
    from _automate import fallback
    assert fallback
else:
    MAIN_PATH = os.path.join(CURRENT_DIR, '_automate', 'main.py')
    # Creating MAIN_PATH if not exists
    if not os.path.isfile(MAIN_PATH):
        print(f'🤖 Creating {MAIN_PATH}', file=sys.stderr)
        shutil.copyfile(FALLBACK_PATH, MAIN_PATH)
    # Load MAIN_PATH and fallback to FALLBACK_PATH
    try:
        print('🤖 Load _automate.main', file=sys.stderr)
        from _automate import main
        assert main
    except Exception:
        print(
            '🤖 Getting error while importing _automate.main', file=sys.stderr
        )
        traceback.print_exc(file=sys.stderr)
        print('🤖 Load _automate.fallback', file=sys.stderr)
        from _automate import fallback
        assert fallback
