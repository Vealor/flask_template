#!/bin/bash

function make_user () {
  curl -H "Content-Type: application/json" -X POST -d '{
    "username":"'$1'",
    "password":"'$2'",
    "email":"'$3'",
    "initials":"'$4'",
    "first_name":"'$5'",
    "last_name":"'$6'",
    "role":"'$7'"
  }' http://localhost:5000/users
}
make_user "test" "test" "lh_test_user@test.test" "TEST" "test_first" "test_last" "tax_master"

make_user "pepperpotts" "test" "pepperpotts@test.test" "pp" "pepper" "potts" "tax_practitioner"
make_user "antman" "test" "antman@test.test" "am" "ant" "man" "tax_practitioner"
make_user "spiderman" "test" "spiderman@test.test" "sm" "spider" "man" "tax_practitioner"
make_user "ironman" "test" "ironman@test.test" "im" "iron" "man" "tax_approver"
make_user "blackpanther" "test" "blackpanther@test.test" "bp" "black" "panther" "tax_approver"
make_user "deadpool" "test" "deadpool@test.test" "dp" "dead" "pool" "tax_approver"
make_user "captainamerica" "test" "captainamerica@test.test" "ca" "captain" "america" "tax_master"
make_user "captainmarvel" "test" "captainmarvel@test.test" "cm" "captain" "marvel" "tax_master"
make_user "lukecage" "test" "lukecage@test.test" "lc" "luke" "cage" "tax_master"
make_user "incrediblehulk" "test" "incrediblehulk@test.test" "ih" "incredible" "hulk" "data_master"
make_user "doctorstrange" "test" "doctorstrange@test.test" "drs" "doctor" "strange" "data_master"
make_user "hawkeye" "test" "hawkeye@test.test" "hwk" "hawk" "eye" "data_master"
make_user "blackwidow" "test" "blackwidow@test.test" "bw" "black" "widow" "administrative_assistant"
make_user "edwinjarvis" "test" "edwinjarvis@test.test" "ej" "edwin" "jarvis" "administrative_assistant"
make_user "philcoulson" "test" "philcoulson@test.test" "pc" "phil" "coulson" "administrative_assistant"
make_user "nickfury" "test" "nickfury@test.test" "nf" "nick" "fury" "tax_practitioner"
