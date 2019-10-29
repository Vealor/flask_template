#!/bin/bash

sudo -i -u postgres psql <<EOF
drop database itra_db;
create database itra_db;
grant all privileges on database itra_db to itra;
EOF

source activate
rm ./migrations/versions/*.py 2> /dev/null
FLASK_ENV='development' flask db migrate
sleep 2
FLASK_ENV='development' flask db upgrade
