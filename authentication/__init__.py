"""
The ETL Library - A Python library for ETL operations with credential management
"""

from .authentication.authentication import Credentials
from .connectors import *

__version__ = "0.1.0"
__author__ = "Your Name"

__all__ = ["Credentials"]
