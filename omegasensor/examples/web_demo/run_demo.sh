#!/bin/bash

export PYTHONPATH=$PYTHONPATH:$(dirname "$0")/../../../
python3 $(dirname "$0")/demo.py
