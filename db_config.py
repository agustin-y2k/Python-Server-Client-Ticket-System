from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from os import getenv
from dotenv import load_dotenv
from sqlalchemy.ext.declarative import declarative_base

# Load the configuration from a .env file when it is present - DB_USER, DB_PASSWORD, DB_NAME
load_dotenv()

# Set the engine configuration - on this case the engine is the starting point for SQLAlchemy
engine = create_engine(f"mysql+pymysql://{getenv('DB_USER')}:{getenv('DB_PASSWORD')}@localhost/{getenv('DB_NAME')}")

# The sessionmaker factory generates new Session objects when called
Session = sessionmaker(bind=engine)

# invokes sessionmaker
session = Session()

'''
The declarative_base() base class contains a MetaData object where newly defined Table objects are collected. This 
object is intended to be accessed directly for MetaData-specific operations. Such as, to issue CREATE statements 
for all tables
'''
Base = declarative_base(bind=engine)
