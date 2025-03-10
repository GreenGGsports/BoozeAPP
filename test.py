from sqlalchemy import Column, Integer, String, ForeignKey, create_engine, inspect
from sqlalchemy.orm import relationship, sessionmaker, declarative_base

Base = declarative_base()

# Static related models
class Company(Base):
    __tablename__ = 'company'
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)

class Invoice(Base):
    __tablename__ = 'invoice'
    id = Column(Integer, primary_key=True)
    amount = Column(Integer, nullable=False)

# Base Factory for Dynamic Models
class BaseModelFactory:
    """
    A base class for dynamically creating models with conditional relationships.
    """

    def __init__(self, engine):
        self.engine = engine
        self.inspector = inspect(engine)

    def table_exists(self, table_name):
        """Check if a table exists in the database."""
        return table_name in self.inspector.get_table_names()

    def create_model(self, model_name, required_fields, relationships):
        """
        Creates a model dynamically.
        :param model_name: Name of the model (used as table name).
        :param required_fields: Dictionary of required column definitions.
        :param relationships: Dictionary of possible relationships.
        """
        fields = {'__tablename__': model_name.lower(), **required_fields}

        # Conditionally add relationships
        for rel_name, rel_details in relationships.items():
            table_name = rel_details['table']
            foreign_key = rel_details['foreign_key']
            related_model = rel_details['model']

            if self.table_exists(table_name):
                fields[foreign_key] = Column(Integer, ForeignKey(f"{table_name}.id"))
                fields[rel_name] = relationship(related_model, backref=f"{model_name.lower()}s")

        # Create and return the dynamic model
        return type(model_name, (Base,), fields)

# Set up the database
engine = create_engine("sqlite:///:memory:")
Base.metadata.create_all(engine)  # Creates the tables

# Initialize the base factory
factory = BaseModelFactory(engine)

# Create Customer Model dynamically
customer_fields = {
    'id': Column(Integer, primary_key=True),
    'name': Column(String(50), nullable=False),
    'email': Column(String(100), nullable=False),
    'age': Column(Integer, nullable=False),
}

customer_relationships = {
    'company': {'table': 'company', 'foreign_key': 'company_id', 'model': 'Company'},
    'invoice': {'table': 'invoice', 'foreign_key': 'invoice_id', 'model': 'Invoice'},
}

Customer = factory.create_model("Customer", customer_fields, customer_relationships)

# Create another dynamic model with different relationships
order_fields = {
    'id': Column(Integer, primary_key=True),
    'order_number': Column(String(50), nullable=False),
}

order_relationships = {
    'customer': {'table': 'customer', 'foreign_key': 'customer_id', 'model': 'Customer'},
}

Order = factory.create_model("Order", order_fields, order_relationships)

# Print generated columns and relationships for validation
print("Customer columns:", Customer.__table__.columns.keys())
print("Customer relationships:", Customer.__mapper__.relationships.keys())
print("Order columns:", Order.__table__.columns.keys())
print("Order relationships:", Order.__mapper__.relationships.keys())
