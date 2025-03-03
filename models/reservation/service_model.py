from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from .base import Base  # Import the shared Base

class ServiceModel(Base):
    __tablename__ = 'service'

    id = Column(Integer, primary_key=True)
    service_name = Column(String(64), nullable=False)
    price_per_slot = Column(Integer, nullable=False)
    description = Column(String(512), nullable=True)
    location_id = Column(Integer, ForeignKey('location.id'), nullable=True)  # Fixed 'locaton' typo

    location = relationship("LocationModel", backref="services")
    slots = relationship('SlotModel', backref='service')

    def __repr__(self):
        return f"<Service {self.service_name}>"
