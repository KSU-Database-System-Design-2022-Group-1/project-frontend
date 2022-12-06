# KStore Frontend

## Launching

The front end is served using a Flask server.  
To launch said Flask server, run:

```
cd new-frontend
flask run
```

The site will then be accessible at the address http://localhost:5000

## Dependencies

To install dependencies, run the following:

```
cd new-frontend
python -m pip install -r requirements.txt
```

## Backend connection

The Flask API server must be running, as well as MariaDB hosting the `kstores` database

For further details, please see the project-backend repository (https://github.com/KSU-Database-System-Design-2022-Group-1/project-backend)
