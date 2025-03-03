
# Import models to ensure they are registered
from .reservation_model import ReservationModel
from .service_model import ServiceModel
from .service_slot import SlotModel
from .customer_model import CustomerModel
from .location_model import LocationModel
from .base import Base

# Explicitly define what gets imported when using `from models import *`
__all__ = ["Base", "ReservationModel", "ServiceModel", "SlotModel", "CustomerModel", "LocationModel"]
