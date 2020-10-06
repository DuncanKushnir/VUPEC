import sys, os

cwd = os.getcwd()
src_dir = os.path.join(cwd, 'src')
print(f'Setting up environment paths for Windows based in: {cwd}')
sys.path.append(src_dir)

from gui import app

app.run(suppress_output=False, override_host="0.0.0.0", override_port=5000)

