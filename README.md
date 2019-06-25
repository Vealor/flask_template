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

### Init
```
./init.sh
```

### Development
```
source activate
python app.py dev
```

Dev with SSL:
```
source activate
python app.py dev ssl
```

Prod test:
```
source activate
python app.py
```

Prod test with ssl:
```
source activate
python app.py ssl
```

## DB Stuff
```
flask db init
```
```
flask db migrate
```
```
flask db --help
```
