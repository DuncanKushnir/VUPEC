:: conda update -n base -c defaults conda
conda create -y --name VUPEC
conda install --force-reinstall -y -q --name VUPEC --file requirements.txt

