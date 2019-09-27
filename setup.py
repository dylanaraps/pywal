"""wal - setup.py"""
import sys
import setuptools

try:
    import pywal
except ImportError:
    print("error: pywal requires Python 3.5 or greater.")
    sys.exit(1)

LONG_DESC = open('README.md').read()
VERSION = pywal.__version__
DOWNLOAD = "https://github.com/dylanaraps/pywal/archive/%s.tar.gz" % VERSION

setuptools.setup(
    name="pywal",
    version=VERSION,
    author="Dylan Araps",
    author_email="dylan.araps@gmail.com",
    description="Generate and change color-schemes on the fly",
    long_description_content_type="text/markdown",
    long_description=LONG_DESC,
    keywords="wal colorscheme terminal-emulators changing-colorschemes",
    license="MIT",
    url="https://github.com/dylanaraps/pywal",
    download_url=DOWNLOAD,
    classifiers=[
        "Environment :: X11 Applications",
        "License :: OSI Approved :: MIT License",
        "Operating System :: POSIX :: Linux",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
    ],
    packages=["pywal"],
    entry_points={"console_scripts": ["wal=pywal.__main__:main"]},
    python_requires=">=3.5",
    test_suite="tests",
    include_package_data=True,
    zip_safe=False)
