# ITRA - API Backend
<!-- <strong>Engagement Code:</strong> xxxxx
<strong>Data Connection:</strong> xxxx:xxxx
___

#### High level description of the project
(Include the purpose of the project)

#### Client Information
(Include client name and background information)

#### Project Value
(What kind of value the project brings)

___
#### Scope
(Include detailed information or reference for the scope of the project)

#### Success Criteria
(Define exact success criteria for the project)

#### Deliverable
(Describe the client's expected deliverable for the project)

___
#### Client Contact Information
(How to contact client and their information) -->


___
## Application Setup
<strong>NOTE: ALL INSTRUCTIONS IN HERE ARE INTENDED FOR BASH ON UBUNTU 16.04 LTS</strong>

### Init
Initialize virtual environment
```
./init.sh
```

### Database Setup
**1.** Enter PSQL => `sudo -i -u postgres psql`
**2.** Create Database => `CREATE DATABASE itra_db;`
**3.** Create User => `CREATE USER itra LOGIN SUPERUSER ENCRYPTED PASSWORD 'LHDEV1234';`
**4.** Grant User Access => `GRANT ALL PRIVILEGES ON DATABASE itra_db TO itra;`
**5.** Quit PSQL => `\q`
**6.** Apply migrations => `./db_refresh.sh`

To get back to PSQL for that DB => `psql -h localhost -U itra itra_db`

Diagnostics => `flask db --help`
___
## Development Server
```
./dev_srv.sh
```

Dev with SSL => `./dev_srv.sh ssl`
___
## Tests, Linting, Code Coverage

stuff about `./runtests.sh cov lint full`

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

___
### Cloud Credentials
**VM Playground**
bash: `ssh lh_admin_tax@40.82.190.135`
password: `Kpmg1234@Kpmg1234@``

**Database Server**
bash: `psql --host=itra-uat-sql.postgres.database.azure.com --port=5432 --username=lh_admin_tax@itra-uat-sql --dbname=itra_db`
password: `Kpmg1234@``

**ITRA Backend**
user = lh-admin-tax
password: Kpmg1234$
