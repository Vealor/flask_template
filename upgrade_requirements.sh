
# This script takes your current versions of installed packages and checks for
# updates, then updates the requirements.txt file.

# Before running this, make sure that you have got any new updates that someone
# may have commit to requirements.txt so that you are not overwriting changes.

source activate
pip list --outdated --format=freeze | grep -v '^\-e' | cut -d = -f 1  | xargs -n1 pip install -U
pip freeze > requirements.txt
