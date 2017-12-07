#!/bin/sh

DIR_HOME=$(pwd)

export PYTHONPATH="${PYTHONPATH}:$DIR_HOME"

python3 regret/run.py
