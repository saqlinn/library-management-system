from sqlalchemy import create_engine, URL
from sqlalchemy.orm import sessionmaker, declarative_base

DATABASE_URL = URL.create(
    drivername="mysql+pymysql",
    username="root",
    password="Saqlin@$2006",
    host="localhost",
    database="library_py"
)

engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

Base = declarative_base()