"""Test __main__ functions."""
import unittest
import unittest.mock

import os

from pywal import __main__
from pywal import reload
from pywal import wallpaper
from pywal import util
from pywal.settings import CACHE_DIR


class TestMain(unittest.TestCase):
    """Test the gen_colors functions."""

    def test_args_a(self):
        """> Test arg parsing (-a)."""
        args = __main__.get_args(["-a", "50"])
        __main__.process_args(args)
        self.assertEqual(util.Color.alpha_num, "50")

    def test_args_c(self):
        """> Test arg parsing (-c)."""
        args = __main__.get_args(["-c"])
        __main__.process_args(args)
        scheme_dir = os.path.join(CACHE_DIR, "schemes")
        self.assertFalse(os.path.isdir(scheme_dir))

    def test_args_e(self):
        """> Test arg parsing (-e)."""
        reload.env = unittest.mock.MagicMock()
        args = __main__.get_args(["-e"])
        __main__.process_args(args)
        self.assertFalse(reload.env.called)

    def test_args_n(self):
        """> Test arg parsing (-n)."""
        wallpaper.change = unittest.mock.MagicMock()
        args = __main__.get_args(["-n"])
        __main__.process_args(args)
        self.assertFalse(wallpaper.change.called)


if __name__ == "__main__":
    unittest.main()
