source activate  # ensure tests are done in virtualenv
export FLASK_ENV=development  # force to development for local testing

test_args=""  # init var
markers=""    # init var

# All modules in src/endpoints need to be specified if you want to have
# separated test markers for each endpoint
modules=(
  auth
  general
  logs
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
if [ -n "${DO_COVERAGE+1}" ]; then
  test_args+=" --cov"
fi
if [ -n "${DO_LINT+1}" ]; then
  test_args+=" --flake8 --cache-clear"
fi
if [ -n "${DO_FULL+1}" ]; then
  test_args+=" -rP"
fi
if [ -n "${DO_NODB+1}" ]; then
  echo $DO_NODB
  test_args+=" --nodb"
fi

for i in "${modules[@]}"; do
  marker="do_${i}"
  if [ -n "${!marker+1}" ]; then
    markers+=" ${i}"
  fi
done

test_args+=" -W ignore::PendingDeprecationWarning"
markers=`echo $markers|sed 's/\ /\ or\ /g'`
py.test -v ${test_args} -m "${markers}" --color=yes
