from setuptools import setup, find_packages
import sys
from ask4args import __version__
"""
linux:
rm -rf "dist/*";rm -rf "build/*";python3 setup.py bdist_wheel;twine upload "dist/*;rm -rf "dist/*";rm -rf "build/*""
win32-git-bash:
rm -rf dist;rm -rf build;python3 setup.py bdist_wheel;twine upload "dist/*";rm -rf dist;rm -rf build;rm -rf ask4args.egg-info
"""
version = __version__
if sys.version_info < (3, 7):
    sys.exit("requires Python 3.7+")
py_version = sys.version_info
install_requires = ["PyInquirer", "pysimplegui", "pydantic"]
with open("README.md", encoding="utf-8") as f:
    README = f.read()

setup(
    name="ask4args",
    version=version,
    keywords=("fire", "REPL", "Terminal UI"),
    description=
    "Python-Fire-like, ask for function args by Terminal UI / GUI, ensuring the type annotation. Read more: https://github.com/ClericPy/ask4args.",
    license="MIT License",
    install_requires=install_requires,
    long_description=README,
    long_description_content_type="text/markdown",
    py_modules=["ask4args"],
    author="ClericPy",
    author_email="clericpy@gmail.com",
    url="https://github.com/ClericPy/ask4args",
    packages=find_packages(),
    platforms="any",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
    ],
)
