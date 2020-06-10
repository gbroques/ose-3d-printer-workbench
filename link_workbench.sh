#!/bin/sh
# ------------------------------------------------------------- #
# Create a symbolic link of workbench to FreeCAD Mod directory. #
# ------------------------------------------------------------- #

set -x  # Print shell command before executing
set -e  # Exit shell script upon non-zero status code (error) of command

# Create temporary python script to find user's FreeCAD Mod directory
touch find_mod_dir.py
echo "import FreeCAD" >> find_mod_dir.py
echo "print App.getUserAppDataDir() + 'Mod'" >> find_mod_dir.py
echo "exit(0)" >> find_mod_dir.py

# TODO: Check if freecad command is available before executing
mod_dir=`freecad -c find_mod_dir.py | tail -1`

# Clean-up temporary python script and .pyc file
rm find_mod_dir.py*

# Soft link workbench repository to user's FreeCAD Mod directory
ln -s $(pwd) $mod_dir/ose-3d-printer-workbench
