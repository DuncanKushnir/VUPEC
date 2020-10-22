"""
This file is a shim to allow the program to function on a WSGI interface for an Apache server
"""

import sys
import os
this_dir = os.path.dirname(os.path.abspath(__file__))
src_dir = os.sep.join([this_dir, 'src'])

activate_this = os.sep.join([this_dir, 'venv/bin/activate_this.py'])
with open(activate_this) as file_:
    exec(file_.read(), dict(__file__=activate_this))


sys.path.insert(0, src_dir)
sys.path.append(this_dir)

from gui.app import app as application
