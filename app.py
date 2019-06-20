import sys
from src import api
from src.util import *

if __name__ == "__main__":
    if len(sys.argv) > 1:
        if sys.argv[1].lower() == "dev":
            if len(sys.argv) > 2 and sys.argv[2].lower() == "ssl":
                print(bcolours.OKGREEN + "\n %% DEV SSL %% \n"+ bcolours.ENDC)
                api.run(debug=True,ssl_context='adhoc')
            else:
                print(bcolours.OKGREEN + "\n %% DEV %% \n"+ bcolours.ENDC)
                api.run(debug=True)
    elif sys.argv[1].lower() == "ssl":
        print(bcolours.OKBLUE + "\n %% PROD %% \n"+ bcolours.ENDC)
        api.run(ssl_context='adhoc')
    else:
        print(bcolours.OKBLUE + "\n %% PROD %% \n"+ bcolours.ENDC)
        api.run()
