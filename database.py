from sqlalchemy import create_engine, text
import os
from models.app import Base  # Import Base from models.app
from modules import import_base

def create_db(db_name, module, db_type="sqlite"):
    """
    Creates a new database based on the selected module.
    Supports SQLite and MySQL.

    :param db_name: Database name
    :param module: Selected module to import the Base from
    :param db_type: "sqlite" or "mysql"
    :return: Database connection string
    """
    if db_type == "mysql":
        db_url = f"mysql+pymysql://root:password@localhost/{db_name}"
        engine = create_engine("mysql+pymysql://root:password@localhost/")  # Update credentials

        with engine.connect() as conn:
            conn.execute(text(f"CREATE DATABASE IF NOT EXISTS {db_name};"))

    elif db_type == "sqlite":
        db_path = f"db/{db_name}.db"
        os.makedirs("db", exist_ok=True)
        db_url = f"sqlite:///{db_path}"

    else:
        raise ValueError("Unsupported database type")

    try:
        Base = import_base(module_name=module)
    
    except Exception as e:
        raise ValueError(f"Unsupported module: {module} , {e}")

    # Create engine and bind the correct Base
    engine = create_engine(db_url)
    Base.metadata.create_all(engine)  # Creates tables using Base

    return db_url


def create_customer_db(customer_id, module, db_type="sqlite"):
    """
    Creates a new database for the customer based on the selected module.
    Supports SQLite and MySQL.

    :param customer_id: Unique customer identifier
    :param module: Selected module (ModuleEnum)
    :param db_type: "sqlite" or "mysql"
    :return: Database connection string
    """
    db_name = f"customer_{customer_id}"

    # Call the refactored create_db function
    return create_db(db_name, module, db_type)


def create_app_db(db_type="sqlite"):
    """
    Creates a new application-wide database.
    Supports SQLite and MySQL.

    :param db_type: "sqlite" or "mysql"
    :return: Database connection string
    """
    db_name = "app_db"

    # Call the refactored create_db function
    return create_db(db_name, "app", db_type)
