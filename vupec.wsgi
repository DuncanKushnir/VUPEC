"""
This file is a shim to allow the program to function on a WSGI interface for an Apache server.
Requires mod_wsgi to be compiled against a python >3.6 target, or use
sudo apt-get install libapache2-mod-wsgi-py3 to replace the standard mod_wsgi target.
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

print("used this command to activate:", activate_this)
print("Running on python", sys.version)
print("Interpreter", sys.executable)
print("Set up with source dir", src_dir)

from gui.app import app as application
