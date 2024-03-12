import os
from dotenv import load_dotenv

load_dotenv()

def get_connect_string():
    engine = os.environ.get("DB_ENGINE")
    dbhost = os.environ.get("DB_HOST")
    username = os.environ.get("DB_USERNAME")
    password = os.environ.get("DB_PASSWORD")
    dbname = os.environ.get("DB_NAME")
    port = os.environ.get("DB_PORT", "5432")
    return f"{engine}://{username}:{password}@{dbhost}:{port}/{dbname}"

SQLALCHEMY_DATABASE_URL= get_connect_string()