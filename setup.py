"""wal - setup.py"""
from setuptools import setup


DESC = (
    "View the README at: https://github.com/dylanaraps/wal.py\n\n"
    "Pypi doesn't like markdown OR rst with anchor links so "
    "you'll have to view the documentation elsewhere.\n"
)
DESC = "".join(DESC)


setup(
    name="pywal",
    version="0.1.3",
    author="Dylan Araps",
    author_email="dylan.araps@gmail.com",
    description="🎨 Generate and change colorschemes on the fly",
    long_description=DESC,
    license="MIT",
    url="https://github.com/dylanaraps/wal.py",
    download_url="https://github.com/dylanaraps/wal.py/archive/0.1.3.tar.gz",
    scripts=["wal"]
)
