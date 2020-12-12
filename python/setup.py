import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

with open("requirements.txt", "r") as f:
    REQUIREMENTS = f.read()

setuptools.setup(
    name="aoc",
    version="0.0.1",
    author="Amir Shahroudy",
    author_email="shahroudy@gmail.com",
    description="My python package including my solutions to the puzzles of 'Advent of Code'",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/shahroudy/Advent-of-Code",
    install_requires=REQUIREMENTS,
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
