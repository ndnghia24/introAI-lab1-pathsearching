#!/bin/bash

python -m pip install --upgrade pip
pip install pygame argparse imageio numpy

python source/main.py
rmdir /s source/noBonus_algorithms/__pycache__