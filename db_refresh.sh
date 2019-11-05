#!/bin/bash


DB_URL=localhost #1
FLASK_ENV=development #2  development, testing, production

USERNAME=itra #3
DATABASE=itra_db #4
PASSWORD=LHDEV1234 #5

BACKEND=localhost #6


################################################################################
SYSTEM="\n[\e[34mSYSTEM\e[39m]"
BASE="\n[\e[92mBASE\e[39m]\t"
FAKE="\n[\e[93mFAKE\e[39m]\t"

sleep 1 && echo -e "$SYSTEM\tRebuilding Database" && sleep 1
./db_scripts/db_rebuild.sh $DB_URL $FLASK_ENV $USERNAME $DATABASE $PASSWORD $BACKEND

printf "\n" && read -n 1 -s -r -p "START SERVER NOW >> Press any key to continue once started" && printf "\n"

sleep 1 && echo -e "$BASE\tCreating initial users" && sleep 1
./db_scripts/create_users.sh $DB_URL $FLASK_ENV $USERNAME $DATABASE $PASSWORD $BACKEND

sleep 1 && echo -e "$FAKE\tInserting base fake data" && sleep 1
./db_scripts/_insert_base_fake_data.sh $DB_URL $FLASK_ENV $USERNAME $DATABASE $PASSWORD $BACKEND

sleep 1 && echo -e "$BASE\tInserting Codes" && sleep 1
./db_scripts/insert_codes.sh $DB_URL $FLASK_ENV $USERNAME $DATABASE $PASSWORD $BACKEND
sleep 1 && echo -e "$BASE\tInserting paredown rules" && sleep 1
./db_scripts/insert_paredown_rules.sh $DB_URL $FLASK_ENV $USERNAME $DATABASE $PASSWORD $BACKEND

sleep 1 && echo -e "$BASE\tInserting CDM labels" && sleep 1
./db_scripts/insert_cdm_labels.sh $DB_URL $FLASK_ENV $USERNAME $DATABASE $PASSWORD $BACKEND

sleep 1 && echo -e "$FAKE\tInserting Nexen data mappings" && sleep 1
./db_scripts/_insert_nexen_data_mappings.sh $DB_URL $FLASK_ENV $USERNAME $DATABASE $PASSWORD $BACKEND

sleep 1 && echo -e "$FAKE\tInserting Nexen data mappings - EMPTY CAPSGEN MAPPING" && sleep 1
./db_scripts/_insert_nexen_data_mappings_mk2.sh $DB_URL $FLASK_ENV $USERNAME $DATABASE $PASSWORD $BACKEND
