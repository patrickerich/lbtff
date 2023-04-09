"""
Version information
"""

import platform
from lbtff import __version__


def get_version():
    """Return package-name __version__ python python_version."""
    return (f'lbtff {__version__} '
            f'python {platform.python_version()}')
