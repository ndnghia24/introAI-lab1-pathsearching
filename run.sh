#!/bin/bash

cd "$(dirname "$0")"

python3 -m pip install --upgrade pip
pip install pygame argparse imageio numpy

python3 source/main.py
rmdir /s source/noBonus_algorithms/__pycache__