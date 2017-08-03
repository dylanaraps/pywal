"""Test __main__ functions."""
import unittest
from unittest.mock import MagicMock

from pywal import __main__
from pywal import reload
from pywal.settings import CACHE_DIR


class TestMain(unittest.TestCase):
    """Test the gen_colors functions."""

    def test_clean(self):
        """> Test arg parsing (-c)"""
        args = __main__.get_args(["-c"])
        __main__.process_args(args)
        self.assertFalse((CACHE_DIR / "schemes").is_dir())

    def test_args_e(self):
        """> Test arg parsing (-e)"""
        reload.env = MagicMock()
        args = __main__.get_args(["-e"])
        __main__.process_args(args)
        self.assertFalse(reload.env.called)


if __name__ == "__main__":
    unittest.main()
