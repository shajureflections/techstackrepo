import os
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
from dotenv import load_dotenv

load_dotenv(override=True)
key = os.environ


def database_config():
    """
    Integrating POSTGRES sql database to the flask
    """

    engine = create_engine(
        f"postgresql+psycopg2://{key['DB_USER']}:{key['DB_PASS']}@{key['DB_HOST']}/{key['TS_DB_NAME']}",
        connect_args={"connect_timeout": 10},
        pool_size=int(key["POOL_SIZE"]),
        echo=False,
    )
    print(f"Integrated PostgresSQL {key['TS_DB_NAME']} Database")
    Session = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    Base = declarative_base()
    return Base, engine, Session
