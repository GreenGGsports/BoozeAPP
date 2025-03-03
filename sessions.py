from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
import os
from flask import request

# Dictionary to store different engine instances for each customer
engine_dict = {}

def get_engine(db_name, db_type="sqlite"):
    if db_type == "mysql":
        db_url = f"mysql+pymysql://root:password@localhost/{db_name}"
    elif db_type == "sqlite":
        db_path = f"db/{db_name}.db"
        os.makedirs("db", exist_ok=True)
        db_url = f"sqlite:///{db_path}"
    else:
        raise ValueError("Unsupported database type")

    # Check if the engine for this db_name already exists, otherwise create a new one
    if db_name not in engine_dict:
        engine_dict[db_name] = create_engine(db_url)

    return engine_dict[db_name]


def get_engine_for_customer(customer_id, db_type="sqlite"):
    # Generate the db_name for the customer
    db_name = f"customer_{customer_id}"

    # You can add logic here to create the customer database if needed for MySQL
    if db_type == "mysql":
        engine = get_engine(db_name, db_type)
        # You can add custom logic here to create the database in MySQL if it doesn't exist
        with engine.connect() as conn:
            conn.execute(f"CREATE DATABASE IF NOT EXISTS {db_name};")
    else:
        # For SQLite, the file will be created automatically by SQLAlchemy when you create the engine
        engine = get_engine(db_name, db_type)

    return engine


# Create a scoped session for a customer
def get_session_for_customer(customer_id, db_type="sqlite"):
    engine = get_engine_for_customer(customer_id, db_type)
    
    # Create a sessionmaker bound to this specific engine
    Session = scoped_session(sessionmaker(bind=engine))

    return Session

# Create a scoped session for a customer
def get_session_for_app(db_name = "app_db", db_type="sqlite"):
    """
    Returns a scoped session for the customer database.
    Creates a new session or reuses an existing session if already created.

    :param customer_id: Unique customer identifier
    :param db_type: "sqlite" or "mysql"
    :return: Scoped session for the customer database
    """
    if db_type == "mysql":
        engine = get_engine(db_name, db_type)
        # You can add custom logic here to create the database in MySQL if it doesn't exist
        with engine.connect() as conn:
            conn.execute(f"CREATE DATABASE IF NOT EXISTS {db_name};")
    else:
        # For SQLite, the file will be created automatically by SQLAlchemy when you create the engine
        engine = get_engine(db_name, db_type)
    
    # Create a sessionmaker bound to this specific engine
    Session = scoped_session(sessionmaker(bind=engine))

    return Session

# Assume that we have a function to get the customer ID from the request (e.g., from a session or a token)
def get_current_customer_id():
    # This could be based on a session or token or something else
    return request.args.get('customer_id')

