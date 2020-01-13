if [[ `command -v unbuffer` ]]; then echo "Expect installed already"; else sudo apt install expect; fi

sudo pip3 install virtualenv
virtualenv -p python3 .venv && source .venv/bin/activate && pip install -r requirements.txt
ln -s .venv/bin/activate ./activate
