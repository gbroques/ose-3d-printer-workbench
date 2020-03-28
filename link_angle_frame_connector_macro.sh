#!/bin/sh
# --------------------------------------------------------------------------------- #
# Create a symbolic link of AngleFrameConnector.FCMacro to FreeCAD macro directory. #
# --------------------------------------------------------------------------------- #

set -x  # Print shell command before executing
set -e  # Exit shell script upon non-zero status code (error) of command

# Create temporary python script to find user's FreeCAD Macro directory
touch find_macro_dir.py
echo "import FreeCAD" >> find_macro_dir.py
echo "print FreeCAD.getUserMacroDir(True)" >> find_macro_dir.py
echo "exit(0)" >> find_macro_dir.py

# TODO: Check if freecad command is available before executing
macro_dir=`freecad -c find_macro_dir.py | tail -1`

# Clean-up temporary python script and .pyc file
rm find_macro_dir.py*

# Soft link macro from repositiory to user's FreeCAD macro directory
ln -s $(pwd)/AngleFrameConnector.FCMacro $macro_dir/AngleFrameConnector.FCMacro
