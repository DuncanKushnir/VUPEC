"""
This file is a shim to allow the program to function on a WSGI interface for an Apache server
"""

import sys

sys.path.append('~/www/VUPEC')
sys.path.append('~/www/VUPEC/src')

from gui.app import app as application
