import json
import os
import sys

sys.path.append(sys.path[0] + "/..")

# FLASK APP
from src.models import (
    db,
    User,
)  # noqa: E402
from src import api  # noqa: E402

# ==============================================================================
# add new function here for each seed
def seed_users(data):
    print("\n\033[34mSEED Users\033[0m\n")
    with api.app_context():
        try:
            for entry in data:
                new_user = User(
                    email=entry["email"],
                    first_name=entry["first_name"],
                    last_name=entry["last_name"],
                    username=entry["username"],
                    password=User.generate_hash(entry["password"]),
                    initials=entry["initials"],
                    role=entry["role"],
                )
                if "is_system_administrator" in entry.keys():
                    new_user.is_system_administrator = True
                if "is_superuser" in entry.keys():
                    new_user.is_superuser = True
                db.session.add(new_user)
            db.session.commit()
        except Exception as e:
            print("\n\t\033[31mERROR\033[0m => users\n")
            print(e)
            db.session.rollback()


# ==============================================================================
# perform seeding
def do_seed():
    # set active path of this file
    curr_path = os.path.dirname(os.path.realpath(__file__)) + "/"

    # base seed files to be done
    seed_files = ["users.json"]
    for file in seed_files:
        with open(curr_path + file, "r") as json_file:
            data = json.load(json_file)  # noqa: F841
            eval("seed_" + file.split(".")[0] + "(data)")


# ==============================================================================
if __name__ == "__main__":
    do_seed()
