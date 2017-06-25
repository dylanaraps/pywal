"""wal - setup.py"""
from setuptools import setup


DESC = (
    "View the DOCS at: https://github.com/dylanaraps/pywal\n\n"
    "Pypi doesn't like markdown OR rst with anchor links so "
    "you'll have to view the documentation elsewhere.\n"
)
DESC = "".join(DESC)


setup(
    name="pywal",
    version="0.1.6",
    author="Dylan Araps",
    author_email="dylan.araps@gmail.com",
    description="🎨 Generate and change colorschemes on the fly",
    long_description=DESC,
    license="MIT",
    url="https://github.com/dylanaraps/pywal",
    download_url="https://github.com/dylanaraps/pywal/archive/0.1.6.tar.gz",
    scripts=["wal"],
    classifiers=[
        "Environment :: X11 Applications",
        "License :: OSI Approved :: MIT License",
        "Operating System :: POSIX :: Linux",
        "Programming Language :: Python :: 3.6",
    ]
)
