source activate
export FLASK_ENV=development

if [[ $1 == *"cov"* ]]; then
  pytest --cov
else
  pytest
fi
