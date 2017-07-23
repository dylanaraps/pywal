"""Test __main__ functions."""
import unittest
from pywal import __main__


class TestMain(unittest.TestCase):
    """Test the gen_colors functions."""

    def test_no_args(self):
        """> Generate a colorscheme and fail."""
        with self.assertRaises(SystemExit):
            args = __main__.get_args([""])
            __main__.process_args(args)

    def test_conflict(self):
        """> Test arg parsing (-i, -f)"""
        with self.assertRaises(SystemExit):
            args = __main__.get_args(["-i", "-f"])
            __main__.process_args(args)

    def test_version(self):
        """> Test arg parsing (-v)"""
        args = __main__.get_args(["-v"])
        self.assertTrue(args.v)

    def test_quiet(self):
        """> Test arg parsing (-q)"""
        args = __main__.get_args(["-q"])
        self.assertTrue(args.q)

    def test_ext_script(self):
        """> Test arg parsing (-o)"""
        args = __main__.get_args(["-o", "true"])
        self.assertTrue(args.o)

if __name__ == "__main__":
    unittest.main()
