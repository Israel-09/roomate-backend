#!/usr/bin/env python3
from sqlalchemy import Column, Integer, String, ForeignKey, DECIMAL
from models.base_model import BaseModel, Base

class Profile(Base, BaseModel):
    """user model"""
    __tablename__ = 'profiles'

    profile_id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    last_name = Column(String(50), nullable=False)
    first_name = Column(String(50), nullable=False)
    other_name = Column(String(50), nullable=True)
    age = Column(Integer)
    gender = Column(String(50))
    cultural_background = Column(String(255))
    financial_stability = Column(String(50))
    budget_rent = Column(DECIMAL(10, 2))

    def __repr__(self):
        '''string representation of profile'''
        return f'Profile: {self.first_name} {self.last_name}'
