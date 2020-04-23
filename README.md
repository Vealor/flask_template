# Flask API Template

___
## Application Setup

### Init
Initialize virtual environment
```
./init.sh
```

### Database Setup
**1.** Enter PSQL => `sudo -i -u postgres psql`  
**2.** Create Database => `CREATE DATABASE dev_user;`  
**3.** Create User => `CREATE USER dev_user LOGIN SUPERUSER ENCRYPTED PASSWORD 'dev_pass';`  
**4.** Grant User Access => `GRANT ALL PRIVILEGES ON DATABASE dev_db TO dev_user;`  
**5.** Quit PSQL => `\q`  
**6.** Apply migrations => `./db_refresh.sh`  

To get back to PSQL for that DB => `psql -h localhost -U dev_user dev_db`

Diagnostics => `flask db --help`


___
## Development Server
```
./dev_srv.sh
```

Dev with SSL => `./dev_srv.sh ssl`


___
## Tests, Linting, Code Coverage

The main testing script is `./run_tests.sh`.

It has further capabilities to give output on linting, code coverage reports, and a more verbose output.

- <strong style="color:red">The database will typically get dumped and rebuild with seeded data...</strong>  
To prevent this, use the command `nodb` at the end of `./run_tests.sh`.  It is good to run the tests with a fresh DB, but it can slow down test development time if you are doing it each time.
**eg** => `./run_tests.sh nodb`

- In order to further speed up test development time, you can limit the output to be one or a set of modules:  
**eg** => `./run_tests.sh auth users` will run the test suite for auth and users endpoints.

- Add the following to the end of `./run_tests.sh` to get further output:  
`cov` => code coverage  
`lint` => linting with flake8  
`full` => more verbose output for tests

An example running all is: `./run_tests.sh cov lint full`

#### Atom Flake8 Linting
Install https://atom.io/packages/linter-flake8
Go into your atom config file from an option in the top menu.

Add:  
```
"linter-flake8":
  executablePath: "$PROJECT/.venv/bin/flake8"
```


___
## Utility scripts
**upgrade_requirements.sh**
If new packages are added then run this script to add them using this script.  
This script ALSO updates all existing packages.

**Updating models and creating a new migration**
`FLASK_ENV='development' flask db migrate`
