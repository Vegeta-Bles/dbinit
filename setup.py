"""Setup configuration for dbinit."""

from setuptools import setup, find_packages
from pathlib import Path

# Read README for long description
readme_file = Path(__file__).parent / "README.md"
long_description = readme_file.read_text() if readme_file.exists() else ""

setup(
    name="dbinit",
    version="0.2.3",
    description="Interactive database initialization tool",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Seth Pang",
    author_email="pang.seth@example.com",
    url="https://github.com/Vegeta-Bles/dbinit",
    license="MIT",
    license_files=["LICENSE"],
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
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
)
