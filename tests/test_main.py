"""Test __main__ functions."""
import unittest
import os

from pywal import __main__
from pywal.settings import __cache_dir__


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

    def test_alpha(self):
        """> Test arg parsing (-a)"""
        args = __main__.get_args(["-a", "99"])
        __main__.process_args(args)
        self.assertTrue(args.a)

    def test_ext_script(self):
        """> Test arg parsing (-o)"""
        args = __main__.get_args(["-o", "true"])
        __main__.process_args(args)
        self.assertTrue(args.o)

    def test_clean(self):
        """> Test arg parsing (-c)"""
        args = __main__.get_args(["-c"])
        __main__.process_args(args)
        self.assertFalse(os.path.isdir(__cache_dir__ / "schemes"))

    def test_reload(self):
        """> Test arg parsing (-r)"""
        with self.assertRaises(SystemExit):
            args = __main__.get_args(["-r"])
            __main__.process_args(args)

    def test_image(self):
        """> Test arg parsing (-i)"""
        args = __main__.get_args(["-i", "tests/test_files/test.jpg"])
        __main__.process_args(args)
        self.assertTrue(args.i)

    def test_json(self):
        """> Test arg parsing (-f)"""
        args = __main__.get_args(["-f", "tests/test_files/test_file.json"])
        __main__.process_args(args)
        self.assertTrue(args.f)


if __name__ == "__main__":
    unittest.main()
