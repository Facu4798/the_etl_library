"""
The ETL Library - A Python library for ETL operations with credential management and database connectors
"""

from .authentication import Credentials
from .connectors import MySQLConnector, DTypeMapper

__version__ = "0.1.0"
__author__ = "Your Name"

__all__ = ["Credentials", "MySQLConnector", "DTypeMapper"]
