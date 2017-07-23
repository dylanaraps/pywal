"""Test __main__ functions."""
import unittest
from pywal import __main__


class TestMain(unittest.TestCase):
    """Test the gen_colors functions."""

    def test_main(self):
        """> Test main function."""
        with self.assertRaises(SystemExit):
            __main__.main()

    def test_no_args(self):
        """> Test no args."""
        with self.assertRaises(SystemExit):
            args = __main__.get_args([""])
            __main__.process_args(args)

    def test_conflict(self):
        """> Test arg parsing (-i, -f)"""
        with self.assertRaises(SystemExit):
            args = __main__.get_args(["-i", "file", "-f", "file"])
            __main__.process_args(args)

    def test_version(self):
        """> Test arg parsing (-v)"""
        with self.assertRaises(SystemExit):
            args = __main__.get_args(["-v"])
            __main__.process_args(args)

    def test_quiet(self):
        """> Test arg parsing (-q)"""
        args = __main__.get_args(["-q"])
        __main__.process_args(args)
        self.assertTrue(args.q)

    def test_ext_script(self):
        """> Test arg parsing (-o)"""
        args = __main__.get_args(["-o", "true"])
        __main__.process_args(args)
        self.assertTrue(args.o)


if __name__ == "__main__":
    unittest.main()
