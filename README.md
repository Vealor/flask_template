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
Enter PSQL
```
sudo -i -u postgres psql
```
Create Database
```
CREATE DATABASE itra_db;
```
Create User
```
CREATE USER itra WITH ENCRYPTED PASSWORD 'LHDEV1234';
```
Grant User Access
```
GRANT ALL PRIVILEGES ON DATABASE itra_db TO itra;
```
Quit PSQL
```
\q
```
Apply migrations:
```
./db_refresh.sh
```

___
To get back to PSQL for that DB:
```
psql -h localhost -U itra itra_db
```

___
Diagnostics:
```
flask db --help
```

### Development
```
./dev_srv.sh
```

Dev with SSL:
```
./dev_srv.sh ssl
```

### Utility scripts
<strong>upgrade_requirements.sh</strong>
If new packages are added then run this script to add them using this script.  
This script ALSO updates all existing packages.

### Updating models and creating a new migration
```FLASK_ENV='development' flask db migrate```


### CAPS Generation ###
Use curl requests for the following endpoints

Unzipping:
```
curl --header "Content-Type: application/json"   --request POST   --data '{"project_id": 1, "file_name": "nexen.zip", "system": "sap"}'   http://localhost:5000/sap_caps_gen/unzipping
```

Build Master Tables:
```
curl --header "Content-Type: application/json" --request POST --data '{"project_id": 1, "file_name": "nexen.zip", "user_id": 1, "system": "sap"}' http://localhost:5000/sap_caps_gen/build_master_tables
```

Rename Scheme:
```
curl --header "Content-Type: application/json" --request POST --data '{"project_id": 1}' http://localhost:5000/sap_caps_gen/rename_scheme
```

Data quality check:
```
curl --header "Content-Type: application/json" --request GET --data '{"project_id": 1}' http://localhost:5000/sap_caps_gen/data_quality_check
```

j1_j10:
```
curl --header "Content-Type: application/json" --request POST --data '{"project_id": 1}' http://localhost:5000/sap_caps_gen/j1_j10
```

aps_to_caps:
```
curl --header "Content-Type: application/json" --request POST --data '{"project_id": 1}' http://localhost:5000/sap_caps_gen/aps_to_caps
```
