from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy import  Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship, sessionmaker
from .base import Base


class User(Base):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True)
    user_name = Column(String(30), nullable=False, unique=True)
    password_hash = Column(String(512), nullable=False)
    role = Column(String(20), nullable=False, default='user')
    app_customer_id = Column(Integer, ForeignKey('app_customers.id'), nullable=True)

    # Relationship with AppCustomer
    app_customer = relationship('AppCustomer', back_populates='users')


    def __repr__(self):
        return f"<UserModel(id={self.id}, user_name='{self.user_name}')>"

    @classmethod
    def login(cls, session, user_name: str, password: str):
        user = session.query(cls).filter_by(user_name=user_name).first()
        if user and check_password_hash(user.password_hash, password):
            return user
        return False

    @classmethod
    def check_name_taken(cls, session, user_name: str):
        return session.query(cls).filter_by(user_name=user_name).first() is not None

    @classmethod
    def add_user(cls, session, user_name: str, password: str, role: str = 'user', app_customer_id=None):
        user = cls(
            user_name=user_name,
            password_hash=generate_password_hash(password=password),
            role=role,
            app_customer_id=app_customer_id  # Associate with AppCustomer
        )
        session.add(user)
        session.commit()
        return user
