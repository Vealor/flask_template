#!/bin/bash


################################################################################
# VARS

# DEVELOPMENT
DB_URL=localhost #1
FLASK_ENV=development #2  development, testing, production
USERNAME=dev_user #3
DATABASE=dev_db #4
PASSWORD=dev_pass #5
PORT=5000 #6
BACKEND=http://localhost #7

# TESTING
if [[ $1 == *"test"* ]]; then
  echo "TESTING"
  DB_URL= #1
  FLASK_ENV=testing #2
  USERNAME= #3
  DATABASE= #4
  PASSWORD= #5
  PORT=5000 #6
  BACKEND= #7

# PRODUCTION
elif [[ $1 == *"prod"* ]]; then
  echo "PRODUCTION"
  DB_URL= #1
  FLASK_ENV=production #2
  USERNAME= #3
  DATABASE= #4
  PASSWORD= #5
  PORT=5000 #6
  BACKEND= #7
fi


################################################################################
# BASH Colouring
SYSTEM="\n[\e[34mSYSTEM\e[39m]"
BASE="\n[\e[92mBASE\e[39m]\t"
FAKE="\n[\e[93mFAKE\e[39m]\t"

################################################################################
# REBUILD DATABASE

sleep 1 && echo -e "$SYSTEM\tRebuilding Database" && sleep 1
echo -e "\tDROP DB"
PGPASSWORD=$PASSWORD dropdb -h "$DB_URL" -U $USERNAME $DATABASE
echo -e "\tCREATE DB"
PGPASSWORD=$PASSWORD createdb -h "$DB_URL" -U $USERNAME $DATABASE

source activate
rm ./migrations/versions/*.py 2> /dev/null
FLASK_ENV="$FLASK_ENV" flask db migrate
sleep 2

FLASK_ENV="$FLASK_ENV" flask db upgrade


################################################################################
### SEED DATA
# cdm_labels, codes, paredown_rules, users
#!/bin/bash
export FLASK_ENV=$FLASK_ENV
source activate
python ./seed/_seed_data.py


################################################################################
