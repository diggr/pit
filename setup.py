from setuptools import setup

setup(
    name="pit",
    version="0.1",
    py_modules=["tool"],
    install_requires=["Click",],
    entry_points="""
        [console_scripts]
        pit=tool:cli
    """
)