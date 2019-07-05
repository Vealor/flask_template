source activate
export FLASK_ENV='development'
flask db init
flask db migrate
flask db upgrade
