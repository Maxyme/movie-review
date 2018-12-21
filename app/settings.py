import os
from urllib.parse import urlparse

DATABASE_URL = os.getenv('DATABASE_URL')
db_conn = urlparse(DATABASE_URL)

DB_HOST = db_conn.hostname
DB_PORT = db_conn.port
DB_USER = db_conn.username
DB_PASSWORD = db_conn.password

DB_DATABASE = db_conn.path.replace('/', '')
CSRF_ENABLED = True

# cors config
QUART_CORS_ALLOW_ORIGIN = os.getenv('CORS_ALLOW_ORIGIN', ['http://localhost:3000'])
# setting this for now, because current quart-cors extension has an issue with * (default value!)
QUART_CORS_ALLOW_HEADERS = ['content-type']