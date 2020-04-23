source activate
export FLASK_ENV=development

if [ "$#" -gt 0 ] && [ $1 == 'ssl' ]; then
  python app.py ssl
else
  python app.py
fi
