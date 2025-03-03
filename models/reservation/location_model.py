from sqlalchemy import Column, Integer, String
from.base import Base  # Import the shared Base class

class LocationModel(Base):
    __tablename__ = 'location'  # Fixed typo

    id = Column(Integer, primary_key=True)
    name = Column(String(64), nullable=False)
    address = Column(String(256), nullable=True)

    def __repr__(self):
        return f"<Location {self.name}>"
