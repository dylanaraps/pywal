"""Test __main__ functions."""
import unittest

from pywal import __main__
from pywal.settings import __cache_dir__


class TestMain(unittest.TestCase):
    """Test the gen_colors functions."""

    def test_clean(self):
        """> Test arg parsing (-c)"""
        args = __main__.get_args(["-c"])
        __main__.process_args(args)
        self.assertFalse((__cache_dir__ / "schemes").is_dir())


if __name__ == "__main__":
    unittest.main()
