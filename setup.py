"""Setup configuration for dbinit."""

from setuptools import setup, find_packages
from pathlib import Path

# Read README for long description
readme_file = Path(__file__).parent / "README.md"
long_description = readme_file.read_text() if readme_file.exists() else ""

setup(
    name="dbinit",
    version="0.1.0",
    description="Interactive database initialization tool",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Your Name",
    author_email="pang.seth@example.com",
    url="https://github.com/Vegeta-Bles/dbinit",
    license="MIT",
    packages=find_packages(),
    install_requires=[
        "click>=8.0.0",
    ],
    python_requires=">=3.7",
    entry_points={
        "console_scripts": [
            "dbinit=dbinit.cli:cli",
        ],
    },
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
)
