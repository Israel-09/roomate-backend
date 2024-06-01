#!/usr/bin/env python3
from sqlalchemy import Column, Integer, String, ForeignKey, Boolean
from models.base_model import BaseModel, Base

class Preference(BaseModel, Base):
    """preference model"""
    __tablename__ = 'preferences'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), unique=True)
    cleanliness = Column(String(50))
    noise_tolerance = Column(String(50))
    sleep_schedule = Column(String(50))
    study_habits = Column(String(50))
    social_habits = Column(String(50))
    smoking = Column(String(50))
    dietary_restrictions = Column(String(255))
    hobbies = Column(String(255))
    comfort_with_cultural_diversity = Column(String(50))
    willingness_to_share_expenses = Column(Boolean)


    def __repr__(self):
        '''string representation of prefences'''
        return f'Preferences: My hobbies are {self.hobbies}'