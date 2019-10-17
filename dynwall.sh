#!/bin/sh
FOLDER_PATH=$1
SCRIPT_PATH=$(dirname "$0")
python $SCRIPT_PATH/dynamic-wallpaper.py $FOLDER_PATH

