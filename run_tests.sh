source activate
export FLASK_ENV=development

test_args=""

# check for args
for arg in "$@"
do
    if [[ "$arg" == *"cov"* ]]; then
        DO_COVERAGE=1
    fi
    if [[ "$arg" == *"lint"* ]]; then
        DO_LINT=1
    fi
done

# add args
if [[ -v DO_COVERAGE ]]; then
  test_args+=" --cov"
fi
if [[ -v DO_LINT ]]; then
  test_args+=" --pylint"
fi

unbuffer py.test ${test_args} --color=yes|\
 sed -r 'w /dev/stderr' |\
 sed -r 's/\x1B\[([0-9]{1,2}(;[0-9]{1,2})?)?[m|K]//g' > TEST_RESULTS.log

echo -e "\n\e[34m=====\e[39m RESULTS IN 'TEST_RESULTS.log' \e[34m=====\e[39m\n"
