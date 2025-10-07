"""
Nice Connectives - Tools for finding and analyzing nice connective sets.

A "nice" set of connectives is both complete (can express all Boolean functions)
and independent (no connective is definable from the others).
"""

__version__ = '1.0.0'

# Expose CLI for package usage
from src.cli import main as cli_main

__all__ = ['cli_main']
