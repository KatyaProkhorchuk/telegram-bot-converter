#!/usr/bin/env bash
python3 -m venv env
source env/bin/activate
pip install -r requirements.txt
export TOKENBOTREWIEW=5236391877:AAF14iW9Vwb9z4ofEnnUtxaGImDsRbpVNh4
python3 main.py
