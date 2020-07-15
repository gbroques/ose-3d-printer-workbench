#!/bin/sh
# ------------------------------------------------------------- #
# Create a symbolic link of workbench to FreeCAD Mod directory. #
# ------------------------------------------------------------- #

set -e  # Exit shell script upon non-zero status code (error) of command

if ! [ -x "$(command -v freecad)" ]; then
    echo "freecad command not found."
    exit
fi

app_data_dir=$(freecad -c "import FreeCAD; print(FreeCAD.getUserAppDataDir())")
mod_dir="${app_data_dir}Mod"
repo_name=$(basename $(pwd))

# Soft link workbench repository to user's FreeCAD Mod directory
echo "Linking workbench to FreeCAD Mod directory with:\n"
echo "    ln -s $(pwd) $mod_dir/$repo_name\n"
ln -s $(pwd) $mod_dir/$repo_name
