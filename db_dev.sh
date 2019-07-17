source activate
export FLASK_ENV='development'
flask db migrate
flask db upgrade
