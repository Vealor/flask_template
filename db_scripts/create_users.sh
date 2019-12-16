#!/bin/bash
export FLASK_ENV=$2
source activate
python ./db_scripts/create_users.py
