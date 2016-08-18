from setuptools import setup

setup(
    # https://pythonhosted.org/setuptools/setuptools.html#declaring-dependencies
    install_requires=[
        "beautifulsoup4 >= 4.5.1, < 5",
        "requests >= 2.11.0, < 3"
    ],
)