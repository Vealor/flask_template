import sys
from src import api

# 0.0.0.0 is used to allow passthrough in a virtual machine for dev
if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1].lower() == "ssl":
        api.run(host="0.0.0.0", ssl_context="adhoc")
    else:
        api.run(host="0.0.0.0")
