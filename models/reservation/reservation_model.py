from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey, Enum
from sqlalchemy.orm import relationship
from datetime import datetime
from enum import Enum as PyEnum
from .base import Base  # Import the shared Base

class PaymentEnum(PyEnum):
    CARD = "bankkártya"
    CASH = "készpénz"
    LIST = "listás"
    TRANSACTION = "utalás"

    def __str__(self):
        return self.value


class ReservationModel(Base):
    __tablename__ = 'reservation'

    id = Column(Integer, primary_key=True)
    slot_id = Column(Integer, ForeignKey('slot.id'), nullable=False)
    service_id = Column(Integer, ForeignKey('service.id'), nullable=False)
    customer_id = Column(Integer, ForeignKey('customer.id'), nullable=False)

    reservation_date = Column(DateTime, default=datetime.utcnow, nullable=False)
    
    final_price = Column(Integer)
    payment_method = Column(Enum(PaymentEnum), nullable=False)
    is_completed = Column(Boolean, default=False)
    comment = Column(String(512), nullable=True)

    # Relationships
    slot = relationship("SlotModel")
    service = relationship("ServiceModel")
    customer = relationship('CustomerModel', back_populates='reservations')
    
    def __repr__(self):
        return f"<Reservation {self.id} - {self.reservation_date}>"
