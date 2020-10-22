"""
This file is a shim to allow the program to function on a WSGI interface for an Apache server
"""

import sys
import os
this_dir = os.path.dirname(os.path.abspath(__file__))
src_dir = os.sep.join([this_dir, 'src'])

sys.path.insert(0, src_dir)
sys.path.append(this_dir)

from src.gui.app import app as application
