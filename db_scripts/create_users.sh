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
  }' $9:$8/users
}

function make_system_administrator () {
  curl -H "Content-Type: application/json" -X POST -d '{
    "username":"'$1'",
    "password":"'$2'",
    "email":"'$3'",
    "initials":"'$4'",
    "first_name":"'$5'",
    "last_name":"'$6'",
    "role":"'$7'",
    "is_system_administrator":1
  }' $9:$8/users
}

make_user "test" "test" "lh_test_user@test.test" "TEST" "test_first" "test_last" "tax_master" $6 $7

make_user "pepperpotts" "test" "pepperpotts@test.test" "pp" "pepper" "potts" "tax_practitioner" $6 $7
make_user "antman" "test" "antman@test.test" "am" "ant" "man" "tax_practitioner" $6 $7
make_user "spiderman" "test" "spiderman@test.test" "sm" "spider" "man" "tax_practitioner" $6 $7
make_user "ironman" "test" "ironman@test.test" "im" "iron" "man" "tax_approver" $6 $7
make_user "blackpanther" "test" "blackpanther@test.test" "bp" "black" "panther" "tax_approver" $6 $7
make_user "deadpool" "test" "deadpool@test.test" "dp" "dead" "pool" "tax_approver" $6 $7
make_user "captainamerica" "test" "captainamerica@test.test" "ca" "captain" "america" "tax_master" $6 $7
make_user "captainmarvel" "test" "captainmarvel@test.test" "cm" "captain" "marvel" "tax_master" $6 $7
make_user "lukecage" "test" "lukecage@test.test" "lc" "luke" "cage" "tax_master" $6 $7
make_user "incrediblehulk" "test" "incrediblehulk@test.test" "ih" "incredible" "hulk" "data_master" $6 $7
make_user "doctorstrange" "test" "doctorstrange@test.test" "drs" "doctor" "strange" "data_master" $6 $7
make_user "hawkeye" "test" "hawkeye@test.test" "hwk" "hawk" "eye" "data_master" $6 $7
make_user "blackwidow" "test" "blackwidow@test.test" "bw" "black" "widow" "administrative_assistant" $6 $7
make_user "edwinjarvis" "test" "edwinjarvis@test.test" "ej" "edwin" "jarvis" "administrative_assistant" $6 $7
make_user "philcoulson" "test" "philcoulson@test.test" "pc" "phil" "coulson" "administrative_assistant" $6 $7
make_user "nickfury" "test" "nickfury@test.test" "nf" "nick" "fury" "tax_practitioner" $6 $7

# LH GVA USER
# curl -H "Content-Type: application/json" -X POST -d '{}' $6:$7/auth/create_base_lh_superuser

# ITRA Users
make_system_administrator "ejensen" "ejensen" "ejensen@kpmg.ca" "edj" "Erin" "Jensen" "tax_master" $6 $7
make_system_administrator "nataliakrizbai" "nataliakrizbai" "nataliakrizbai@kpmg.ca" "nk" "Natalia" "Krizbai" "tax_master" $6 $7
make_system_administrator "dcallow" "dcallow" "dcallow@kpmg.ca" "dtc" "Dylan" "Callow" "tax_master" $6 $7
make_system_administrator "ryansen" "ryansen" "ryansen@kpmg.ca" "rjs" "Ryan" "Sen" "tax_master" $6 $7
make_system_administrator "karinadewi" "karinadewi" "karinadewi@kpmg.ca" "kd" "Karina" "Dewi" "tax_master" $6 $7
make_system_administrator "jasonclee" "jasonclee" "jasonclee@kpmg.ca" "jcl" "Jason" "Lee" "tax_master" $6 $7
make_system_administrator "andylee1" "andylee1" "andylee1@kpmg.ca" "al" "Andy" "Lee" "tax_master" $6 $7
