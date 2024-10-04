#!/bin/bash

cd /home/johnny/ckjz
source .venv/bin/activate


exec python -m ckjz.script run --ip 0.0.0.0 --port 8000 --UL1 16 --UL2 12 --UM1 26 --UM2 4

