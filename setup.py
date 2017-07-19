"""wal - setup.py"""
import setuptools

try:
    import pywal
except (ImportError, SyntaxError):
    print("error: pywal requires Python 3.6 or greater.")
    quit(1)


DESC = (
    "View the DOCS at: https://github.com/dylanaraps/pywal\n\n"
    "Pypi doesn't like markdown OR rst with anchor links so "
    "you'll have to view the documentation elsewhere.\n"
)

VERSION = pywal.__version__
DOWNLOAD = "https://github.com/dylanaraps/pywal/archive/%s.tar.gz" % VERSION


setuptools.setup(
    name="pywal",
    version=VERSION,
    author="Dylan Araps",
    author_email="dylan.araps@gmail.com",
    description="Generate and change colorschemes on the fly",
    long_description=DESC,
    license="MIT",
    url="https://github.com/dylanaraps/pywal",
    download_url=DOWNLOAD,
    classifiers=[
        "Environment :: X11 Applications",
        "License :: OSI Approved :: MIT License",
        "Operating System :: POSIX :: Linux",
        "Programming Language :: Python :: 3.6",
    ],
    packages=["pywal"],
    entry_points={
        "console_scripts": ["wal=pywal.__main__:main"]
    },
    python_requires=">=3.6",
    test_suite="tests",
    include_package_data=True
)
