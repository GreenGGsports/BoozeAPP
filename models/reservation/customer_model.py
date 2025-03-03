from sqlalchemy import Column, Integer, DateTime, JSON
from sqlalchemy.orm import relationship
from datetime import datetime
from .base import Base  # Import the shared Base

class CustomerModel(Base):
    __tablename__ = 'customer'

    id = Column(Integer, primary_key=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    # Use JSON for dynamic fields, handles MySQL, PostgreSQL, and SQLite
    data = Column(JSON, nullable=True)  # SQLAlchemy's generic JSON type

    # Relationship with ReservationModel
    reservations = relationship('ReservationModel', back_populates='customer')

    def __repr__(self):
        return f"<Customer {self.id} - {self.data}>"
