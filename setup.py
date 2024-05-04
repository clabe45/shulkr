import os.path
from setuptools import find_packages, setup


script_dir = os.path.dirname(os.path.realpath(__file__))
with open(os.path.join(script_dir, "README.md"), "r") as f:
    README = f.read()

classifiers = [
    "Development Status :: 3 - Alpha",
    "Environment :: Console",
    "Intended Audience :: Developers",
    "Intended Audience :: Science/Research",
    "License :: OSI Approved :: Apache Software License",
    "Operating System :: OS Independent",
    "Programming Language :: Python",
    "Programming Language :: Python :: 3",
    "Topic :: Games/Entertainment",
    "Topic :: Scientific/Engineering",
    "Topic :: Software Development :: Version Control :: Git",
    "Topic :: Utilities",
]

setup(
    name="shulkr",
    version="0.7.2",
    description="Diff decompiled versions of Minecraft",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/clabe45/shulkr",
    author="Caleb Sacks",
    license="GPLv3",
    classifiers=classifiers,
    keywords=["minecraft", "git", "decompile", "game"],
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    py_modules=["colorama", "java", "minecraft", "mint", "shulkr"],
    install_requires=["gitpython", "javalang", "unidiff", "requests", "toml", "click"],
    entry_points={"console_scripts": ["shulkr=shulkr.__main__:main"]},
)
