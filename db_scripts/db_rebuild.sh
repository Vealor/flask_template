#!/bin/bash

echo -e "\tDROP DB"
PGPASSWORD=$5 dropdb -h "$1" -U $3 $4
echo -e "\tCREATE DB"
PGPASSWORD=$5 createdb -h "$1" -U $3 $4

source activate
rm ./migrations/versions/*.py 2> /dev/null
FLASK_ENV="$2" flask db migrate
sleep 2
# CRITICAL ORDER DO NOT MODIFY #################################################
sed -i 's/src.models._enums.ArrayOfEnum/ArrayOfEnum/g' ./migrations/versions/*.py
sed -i 's/from sqlalchemy.dialects import postgresql/from sqlalchemy.dialects import postgresql\nfrom src.models import ArrayOfEnum/g' ./migrations/versions/*.py
sed -i 's/ENUM/postgresql.ENUM/g' ./migrations/versions/*.py
################################################################################
FLASK_ENV="$2" flask db upgrade
