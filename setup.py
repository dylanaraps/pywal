"""wal - setup.py"""
from setuptools import setup


try:
    import pypandoc
    DESC = pypandoc.convert('README.md', 'rst')
    DESC = DESC.replace("\r", "")
except(IOError, ImportError):
    print("README convert to RST failed, using markdown.")
    DESC = open('README.md').read()


setup(
    name="pywal",
    version="0.1.1",
    author="Dylan Araps",
    author_email="dylan.araps@gmail.com",
    description="🎨 Generate and change colorschemes on the fly",
    long_description=DESC,
    license="MIT",
    url="https://github.com/dylanaraps/wal.py",
    download_url="https://github.com/dylanaraps/wal.py/archive/0.1.1.tar.gz",
    scripts=["wal"]
)
