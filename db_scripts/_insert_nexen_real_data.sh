#!/bin/bash

# DEVELOPMENT


DB_URL=localhost #1
FLASK_ENV=development #2  development, testing, production
USERNAME=itra #3
DATABASE=itra_db #4
PASSWORD=LHDEV1234 #5
PORT=5000 #6
BACKEND=http://localhost #7
# TESTING
if [[ $1 == *"test"* ]]; then
  echo "TESTING"
  DB_URL=itra-uat-sql.postgres.database.azure.com #1
  FLASK_ENV=testing #2
  USERNAME=lh_admin_tax@itra-uat-sql.postgres.database.azure.com #3
  DATABASE=itra_db #4
  PASSWORD=Kpmg1234@ #5
  PORT=443 #6
  BACKEND=https://itra-backend-uat.azurewebsites.net #7

# PRODUCTION
elif [[ $1 == *"prod"* ]]; then
  echo "PRODUCTION"
  DB_URL=localhost #1
  FLASK_ENV=production #2
  USERNAME=itra #3
  DATABASE=itra_db #4
  PASSWORD=LHDEV1234 #5
  PORT=5000 #6
  BACKEND=http://localhost #7
fi

PGPASSWORD=$PASSWORD psql -h $DB_URL -U $USERNAME $DATABASE -c "\\copy sap_caps from '../sap_caps.csv' DELIMITER '|' CSV;"
