#!/bin/python

#
#       ███╗   ██╗██╗██╗  ██╗ █████╗ ██████╗ ███████╗
#       ████╗  ██║██║██║  ██║██╔══██╗██╔══██╗██╔════╝
#       ██╔██╗ ██║██║███████║███████║██████╔╝███████╗
#       ██║╚██╗██║██║██╔══██║██╔══██║██╔══██╗╚════██║
#       ██║ ╚████║██║██║  ██║██║  ██║██║  ██║███████║
#       ╚═╝  ╚═══╝╚═╝╚═╝  ╚═╝╚═╝  ╚═╝╚═╝  ╚═╝╚══════╝
#       DRAFTED BY [https://nih.ar] ON 14-04-2025
#       SOURCE [__init__.py] LAST MODIFIED ON 28-04-2025.
#

"""
Module for versioning of the rynz package.

This module defines the version number for the rynz static site generator
and provides a function to retrieve the current version.
"""

__version__ = "1.0.0"

def get_version():
    """Returns the current version of the rynz package."""
    return __version__
