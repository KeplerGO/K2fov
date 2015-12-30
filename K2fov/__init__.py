from __future__ import (division, absolute_import)

import os
import logging
logger = logging.getLogger(__name__)

# Where are the K2 Campaign parameters stored?
PACKAGEDIR = os.path.dirname(os.path.abspath(__file__))

# Optical distortions can cause the results from K2fov to be off by a bit.
# The padding parameter compensates for this; setting padding > 0 means
# that objects that are computed to lie a small amount off silicon will
# be considered on silicon.
DEFAULT_PADDING = 3  # pixels

# Add fields.* and K2onSilicon.K2onSilicon to the root namespace
from .fields import *
from .K2onSilicon import K2onSilicon


class Highlight:
    """Defines colors for highlighting words in the terminal."""
    RED = "\033[0;31m"
    GREEN = "\033[0;32m"
    YELLOW = "\033[0;33m"
    BLUE = "\033[0;34m"
    PURPLE = "\033[0;35m"
    CYAN = "\033[0;36m"
    END = '\033[0m'
