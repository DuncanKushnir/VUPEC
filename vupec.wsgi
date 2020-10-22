"""
This file is a shim to allow the program to function on a WSGI interface for an Apache server
"""

import sys
import os
this_dir = os.path.dirname(os.path.abspath(__file__))
vupec_dir = os.path.dirname(this_dir)

sys.path.append(this_dir)
sys.path.append(vupec_dir)

from gui.app import app as application
