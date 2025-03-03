from sqlalchemy import Table, Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from .base import Base
# Association table for the many-to-many relationship
app_customer_module = Table('app_customer_module', Base.metadata,
    Column('app_customer_id', Integer, ForeignKey('app_customers.id'), primary_key=True),
    Column('module_id', Integer, ForeignKey('module.id'), primary_key=True)
)

class Module(Base):
    __tablename__ = 'module'

    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False)
    path = Column(String(50), nullable=False)

    def __init__(self, name, path):
        self.name = name
        self.path = path
        
    
    def __repr__(self):
        return f"{self.name}"

class AppCustomer(Base):
    __tablename__ = 'app_customers'

    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False)
    email = Column(String(120), nullable=False, unique=True)

    # Use relationship for the many-to-many association
    app_customer_modules = relationship('Module', secondary=app_customer_module, backref='app_customers')
    users = relationship('User', back_populates='app_customer') 
    # Add a relationship to User if needed, assuming User is defined elsewhere
    # users = relationship('User', back_populates='app_customer')
