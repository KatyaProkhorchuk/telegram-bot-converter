#!/usr/bin/env bash
python3 -m venv env
source env/bin/activate
pip install -r requirements.txt
export TOKENBOTREWIEW=""
python3 main.py
