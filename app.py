import sys
from src import api
from src.util import *

if __name__ == "__main__":
    if len(sys.argv) > 1:
        if sys.argv[1].lower() == "dev":
            print(bcolours.OKGREEN + "\n %% DEV %% \n"+ bcolours.ENDC)
            api.run(debug=True,ssl_context='adhoc')
    else:
        print(bcolours.OKBLUE + "\n %% PROD %% \n"+ bcolours.ENDC)
        api.run(ssl_context='adhoc')
