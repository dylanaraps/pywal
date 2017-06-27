"""wal - setup.py"""
from setuptools import setup, find_packages
import pywal


DESC = (
    "View the DOCS at: https://github.com/dylanaraps/pywal\n\n"
    "Pypi doesn't like markdown OR rst with anchor links so "
    "you'll have to view the documentation elsewhere.\n"
)
DESC = "".join(DESC)


VERSION = pywal.__version__
DOWNLOAD_URL = f"https://github.com/dylanaraps/pywal/archive/{VERSION}.tar.gz"


setup(
    name="pywal",
    version=VERSION,
    author="Dylan Araps",
    author_email="dylan.araps@gmail.com",
    description="🎨 Generate and change colorschemes on the fly",
    long_description=DESC,
    license="MIT",
    url="https://github.com/dylanaraps/pywal",
    download_url=DOWNLOAD_URL,
    classifiers=[
        "Environment :: X11 Applications",
        "License :: OSI Approved :: MIT License",
        "Operating System :: POSIX :: Linux",
        "Programming Language :: Python :: 3.6",
    ],
    packages=find_packages(),
    entry_points={
        "console_scripts": ["wal=pywal.__main__:main"]
    },
    python_requires=">=3.6"
)
