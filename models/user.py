#!/usr/bin/env python3
from sqlalchemy import Column, Integer, String
from models.base_model import BaseModel, Base
from sqlalchemy.orm import relationship


class User(BaseModel, Base):
    """user model"""
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, autoincrement=True)
    email = Column(String(50), nullable=False)
    hashed_password = Column(String(250), nullable=False)
    session_id = Column(String(250))
    reset_token = Column(String(250))

    profile = relationship('Profile', uselist=False, backref='users')
    preference = relationship('Preference', uselist=False, backref='users')

    def __repr__(self):
        '''string representation of user'''
        return f'User: {self.email}'