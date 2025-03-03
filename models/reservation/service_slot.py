from sqlalchemy import Column, Integer, DateTime, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from .base import Base  # Import the shared Base

class SlotModel(Base):
    __tablename__ = 'slot'
    
    id = Column(Integer, primary_key=True)
    start_time = Column(DateTime, nullable=False)
    end_time = Column(DateTime, nullable=False)
    live = Column(Boolean, default=True)
    service_id = Column(Integer, ForeignKey('service.id'), nullable=False)

    service = relationship('ServiceModel', back_populates='slots')  # Fixed the relationship

    def __repr__(self):
        return f"Slot(id={self.id}, start_time={self.start_time}, end_time={self.end_time}, live={self.live})"
