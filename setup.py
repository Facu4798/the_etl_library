
from setuptools import setup, find_packages

setup(
    name="la_libreria",
    version="0.1.10",
    description="The ETL Library - A Python library for ETL operations with credential management and database connectors",
    author="Your Name",
    packages=find_packages(),
    install_requires=[
        "numpy",
        "matplotlib",
        "networkx",
        "mysql-connector-python",
        "pandas",
        "graphviz"
    ],
    python_requires=">=3.7",
    include_package_data=True,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
