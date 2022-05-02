"""
Handles converting parsed block data into code

When given an opcode, it gets a BlockMap which handles
formatting parsed inputs and fields into Python code.
"""

from . import codemap
from .specmap import *
from .blockmap import *
