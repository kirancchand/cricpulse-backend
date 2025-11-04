
import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from pathlib import Path
# Load .env from the root directory
env_path = Path(__file__).resolve().parent.parent / ".env"
load_dotenv(dotenv_path=env_path)

DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST")
DB_NAME = os.getenv("DB_NAME")
DB_PORT = os.getenv("DB_PORT")
print("DB_USER:", DB_USER) 
from urllib.parse import quote_plus
encoded_password = quote_plus(DB_PASSWORD)


# DATABASE_URL = f"mysql+mysqlconnector://{DB_USER}:{encoded_password}@{DB_HOST}/{DB_NAME}"
DATABASE_URL = f"mysql+pymysql://{DB_USER}:{encoded_password}@{DB_HOST}:{DB_PORT}/{DB_NAME}"



engine = create_engine(DATABASE_URL, echo=True, future=True)

# engine = create_engine(DATABASE_URL, pool_size=5, pool_pre_ping=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


#************mysql pooling*****#
# import mysql.connector
# from mysql.connector import pooling
# # Connection pool configuration
# db_config = {
#     "host": "localhost",
#     "user": "root",
#     "password": "kiran@89",
#     "database": "cricpulse",
# }

# # Create a connection pool
# connection_pool = pooling.MySQLConnectionPool(pool_name="mypool", pool_size=5, **db_config)

# # Dependency for getting a database connection
# def get_db():
#     conn = connection_pool.get_connection()
#     try:
#         yield conn
#     finally:
#         conn.close()
