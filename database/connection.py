from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
from sqlalchemy_utils import database_exists, create_database
import os

load_dotenv()
from config.settings import (
    POSTGRES_USER,
    POSTGRES_PASSWORD,
    POSTGRES_DB,
    POSTGRES_HOST,
    POSTGRES_PORT
)


DATABASE_URL = (
    f"postgresql://"
    f"{POSTGRES_USER}:"
    f"{POSTGRES_PASSWORD}@"
    f"{POSTGRES_HOST}:"
    f"{POSTGRES_PORT}/"
    f"{POSTGRES_DB}"
)

if not DATABASE_URL:
    raise ValueError("DATABASE_URL is not set")

if not database_exists(DATABASE_URL):
    create_database(DATABASE_URL)
    print("Database created")
else:
    print(f"Database already exists: {DATABASE_URL}")

engine = create_engine(
    DATABASE_URL
)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)