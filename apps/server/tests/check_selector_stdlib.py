"""Run only the selector's synthetic suite without optional dependencies.

Use ``python -B -S tests/check_selector_stdlib.py`` from apps/server.
"""
import importlib.abc
from pathlib import Path
import sys
import unittest

TESTS = Path(__file__).resolve().parent
SERVER = TESTS.parent
sys.path.insert(0, str(SERVER))
sys.path.insert(0, str(TESTS))


class StandardLibraryOnly(importlib.abc.MetaPathFinder):
    def find_spec(self, fullname, path=None, target=None):
        root = fullname.split('.')[0]
        if root not in sys.stdlib_module_names and root not in {
            'kotoba_capture', 'selector_v17'
        }:
            raise ModuleNotFoundError('Nonstdlib import blocked: ' + root)
        return None


sys.meta_path.insert(0, StandardLibraryOnly())
for forbidden in ('numpy', 'cv2', 'paddleocr'):
    try:
        __import__(forbidden)
    except ModuleNotFoundError as error:
        assert str(error) == 'Nonstdlib import blocked: ' + forbidden
    else:
        raise AssertionError('Nonstdlib import blocker failed: ' + forbidden)

# Import the tracked package, never a dynamically loaded experiment file.
from kotoba_capture import selector

assert Path(selector.__file__).resolve() == SERVER / 'kotoba_capture' / 'selector.py'
suite = unittest.defaultTestLoader.discover(
    str(TESTS / 'selector_v17'), top_level_dir=str(TESTS)
)
if suite.countTestCases() != 116:
    raise AssertionError('Expected all 116 synthetic selector tests')
result = unittest.TextTestRunner(verbosity=2).run(suite)
raise SystemExit(not result.wasSuccessful())
