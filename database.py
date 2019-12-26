from orator import DatabaseManager

DATABASES = {
    "default": "mysql",
    "mysql": {
        "driver": "mysql",
        "host": "localhost",
        "database": "seismic",
        "user": "homestead",
        "password": "secret",
        "prefix": ""
    }
}

database = DatabaseManager(DATABASES)