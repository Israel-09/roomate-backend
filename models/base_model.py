#!/usr/bin/env python3
"""
    base model class
"""
from datetime import datetime
from sqlalchemy import Column, DateTime
from sqlalchemy.ext.declarative import declarative_base



Base = declarative_base()

class BaseModel:
    """base model object"""
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now)