from settings import SQLALCHEMY_DATABASE_URL
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

def get_db_context():
    try:
        db = LocalSession()
        yield db
    finally:
        db.close()


engine = create_engine(SQLALCHEMY_DATABASE_URL)
 
LocalSession = sessionmaker(autoflush=False, autocommit=False, bind=engine)

Base = declarative_base()