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
# CRITICAL ORDER DO NOT MODIFY #################################################
sed -i 's/src.models.ArrayOfEnum/ArrayOfEnum/g' ./migrations/versions/*.py
sed -i 's/from sqlalchemy.dialects import postgresql/from sqlalchemy.dialects import postgresql\nfrom src.models import ArrayOfEnum/g' ./migrations/versions/*.py
sed -i 's/ENUM/postgresql.ENUM/g' ./migrations/versions/*.py
################################################################################
FLASK_ENV='development' flask db upgrade
