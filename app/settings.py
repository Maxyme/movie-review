import os

#SQLALCHEMY_DATABASE_URI = os.environ('DATABASE_URL')
DB_HOST = os.getenv('DB_HOST', 'localhost')
DB_PORT = os.getenv('DB_PORT', 5432)
DB_USER = os.getenv('DB_USER', 'postgres')
DB_PASSWORD = os.getenv('DB_PASSWORD', 'test123')
DB_DATABASE = os.getenv('DB_DATABASE', 'movies')
SQLALCHEMY_TRACK_MODIFICATIONS = False
CSRF_ENABLED = True
