source activate
export FLASK_ENV=development

test_args=""
markers=""

modules=(
  auth
  caps_gen
  cdm_labels
  client_models
  client_tax_gl_extract
  client_vendor_master
  clients
  codes
  data_mappings
  data_params
  error_categories
  fx_rates
  general
  gst_registration
  jurisdictions
  lob_sectors
  logs
  master_models
  paredown_rules
  projects
  roles
  tax_rates
  transactions
  users
)

# check for args
for arg in "$@"
do
    if [[ "$arg" == *"nodb"* ]]; then
        DO_NODB=1
    fi
    if [[ "$arg" == *"cov"* ]]; then
        DO_COVERAGE=1
    fi
    if [[ "$arg" == *"lint"* ]]; then
        DO_LINT=1
    fi
    if [[ "$arg" == *"full"* ]]; then
        DO_FULL=1
    fi

    for i in "${modules[@]}"; do
      if [[ "$arg" == *"$i"* ]]; then
        eval "do_$i=1"
      fi
    done
done

# add args
if [[ -v DO_COVERAGE ]]; then
  test_args+=" --cov"
fi
if [[ -v DO_LINT ]]; then
  test_args+=" --flake8 --cache-clear"
fi
if [[ -v DO_FULL ]]; then
  test_args+=" -rP"
fi
if [[ -v DO_NODB ]]; then
  test_args+=" --nodb"
fi

for i in "${modules[@]}"; do
  if [[ -v do_$i ]]; then
    markers+=" ${i}"
  fi
done

test_args+=" -W ignore::PendingDeprecationWarning"

markers=`echo $markers|sed 's/\ /\ or\ /g'`
# echo $markers
unbuffer py.test -v ${test_args} -m "${markers}" --color=yes|\
 sed -r 'w /dev/stderr' |\
 sed -r 's/\x1B\[([0-9]{1,2}(;[0-9]{1,2})?)?[m|K]//g' > TEST_RESULTS.log

echo -e "\n\e[34m=====\e[39m RESULTS IN 'TEST_RESULTS.log' \e[34m=====\e[39m\n"
