#!/usr/bin/python3
"""Initialize the views blueprint"""
from flask import Blueprint

app_views = Blueprint("base", __name__, url_prefix="")

from api.v1.views.user import *
from api.v1.views.sessions import *