#!/bin/bash

# RED=$'\e[31m'
# GREEN=$'\e[92m'
# BLUE=$'\e[34m'
# YELLOW=$'\e[93m'
# DEFAULT=$'\e[39m'
SYSTEM="\n[\e[34mSYSTEM\e[39m]"
BASE="\n[\e[92mBASE\e[39m]\t"
FAKE="\n[\e[93mFAKE\e[39m]\t"

sleep 1 && echo -e "$SYSTEM\tRebuilding Database" && sleep 1
./db_scripts/db_rebuild.sh

printf "\n" && read -n 1 -s -r -p "START SERVER NOW >> Press any key to continue once started" && printf "\n"

sleep 1 && echo -e "$BASE\tCreating initial users" && sleep 1
./db_scripts/create_users.sh

sleep 1 && echo -e "$FAKE\tInserting base fake data" && sleep 1
./db_scripts/_insert_base_fake_data.sh

sleep 1 && echo -e "$BASE\tInserting paredown rules" && sleep 1
./db_scripts/insert_paredown_rules.sh

sleep 1 && echo -e "$BASE\tInserting CDM labels" && sleep 1
./db_scripts/insert_cdm_labels.sh

sleep 1 && echo -e "$BASE\tInserting Codes" && sleep 1
./db_scripts/insert_codes.sh

sleep 1 && echo -e "$FAKE\tInserting Nexen data mappings" && sleep 1
./db_scripts/_insert_nexen_data_mappings.sh

sleep 1 && echo -e "$FAKE\tInserting Nexen data mappings - EMPTY CAPSGEN MAPPING" && sleep 1
./db_scripts/_insert_nexen_data_mappings_mk2.sh
