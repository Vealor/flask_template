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

make_user "itra" "test" "lh_test_user@test.test" "ITRA" "Ozge" "Uncu" "tax_master" $6 $7

make_user "wsmith" "test" "wsmith@test.test" "WS" "William" "Smith" "tax_practitioner" $6 $7
make_user "msmith" "test" "msmith@test.test" "MS" "Morty" "Smith" "tax_practitioner" $6 $7
make_user "radams" "test" "radams@test.test" "RA" "Ryan" "Adams" "tax_practitioner" $6 $7
make_user "mgarcia" "test" "mgarcia@test.test" "MG" "Maria" "Garcia" "tax_approver" $6 $7
make_user "aochoa" "test" "aochoa@test.test" "AO" "Andrea" "Ochoa" "tax_approver" $6 $7
make_user "rpatel" "test" "rpatel@test.test" "RP" "Russell" "Patel" "tax_approver" $6 $7
make_user "creily" "test" "creily@test.test" "CR" "Chris" "Reily" "tax_master" $6 $7
make_user "lxiang" "test" "lxiang@test.test" "LX" "Lisa" "Xiang" "tax_master" $6 $7
make_user "fghosh" "test" "fghosh@test.test" "FG" "Frank" "Ghosh" "tax_master" $6 $7
make_user "jzafar" "test" "jzafar@test.test" "JZ" "Jasmine" "Zafar" "data_master" $6 $7
make_user "ddeguzman" "test" "ddeguzman@test.test" "DDG" "David" "DeGuzman" "data_master" $6 $7
make_user "kvaldo" "test" "kvaldo@test.test" "KV" "Kiara" "Valdo" "data_master" $6 $7
make_user "rsanchez" "test" "rsanchez@test.test" "RS" "Rick" "Sanchez" "administrative_assistant" $6 $7
make_user "psylvester" "test" "psylvester@test.test" "PS" "Pen" "Sylvester" "administrative_assistant" $6 $7
make_user "arails" "test" "arails@test.test" "AR" "Adam" "Rails" "administrative_assistant" $6 $7
make_user "vmaximus" "test" "vmaximus@test.test" "VM" "Vance" "Maximus" "tax_practitioner" $6 $7

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
