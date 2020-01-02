#!/bin/bash

# DEVELOPMENT
DB_URL=localhost #1
FLASK_ENV=development #2  development, testing, production
USERNAME=itra #3
DATABASE=itra_db #4
PASSWORD=LHDEV1234 #5
PORT=5000 #6
BACKEND=http://localhost #7
ID=3

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
  ID=3

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
  ID=3
fi


################################################################################
SYSTEM="\n[\e[34mSYSTEM\e[39m]"
BASE="\n[\e[92mBASE\e[39m]\t"
FAKE="\n[\e[93mFAKE\e[39m]\t"

sleep 1 && echo -e "$SYSTEM\tRebuilding Database" && sleep 1
./db_scripts/db_rebuild.sh $DB_URL $FLASK_ENV $USERNAME $DATABASE $PASSWORD $PORT $BACKEND

sleep 1 && echo -e "$BASE\tCreating initial users" && sleep 1
./db_scripts/create_users.sh $DB_URL $FLASK_ENV $USERNAME $DATABASE $PASSWORD $PORT $BACKEND

sleep 1 && echo -e "$FAKE\tInserting base fake data" && sleep 1
./db_scripts/_insert_base_fake_data.sh $DB_URL $FLASK_ENV $USERNAME $DATABASE $PASSWORD $PORT $BACKEND

sleep 1 && echo -e "$BASE\tInserting Codes" && sleep 1
./db_scripts/insert_codes.sh $DB_URL $FLASK_ENV $USERNAME $DATABASE $PASSWORD $PORT $BACKEND
sleep 1 && echo -e "$BASE\tInserting paredown rules" && sleep 1
./db_scripts/insert_paredown_rules.sh $DB_URL $FLASK_ENV $USERNAME $DATABASE $PASSWORD $PORT $BACKEND

sleep 1 && echo -e "$BASE\tInserting CDM labels" && sleep 1
./db_scripts/insert_cdm_labels.sh $DB_URL $FLASK_ENV $USERNAME $DATABASE $PASSWORD $PORT $BACKEND

sleep 1 && echo -e "$FAKE\tInserting Nexen data mappings" && sleep 1
./db_scripts/_insert_nexen_data_mappings.sh $DB_URL $FLASK_ENV $USERNAME $DATABASE $PASSWORD $PORT $BACKEND $ID

# sleep 1 && echo -e "$FAKE\tInserting Nexen data mappings - EMPTY CAPSGEN MAPPING" && sleep 1
# ./db_scripts/_insert_nexen_data_mappings_mk2.sh $DB_URL $FLASK_ENV $USERNAME $DATABASE $PASSWORD $PORT $BACKEND

#sleep 1 && echo -e "$FAKE\tInserting dummy prediction models" && sleep 1
#./db_scripts/_insert_dummy_prediction_models.sh $DB_URL $FLASK_ENV $USERNAME $DATABASE $PASSWORD $PORT $BACKEND
