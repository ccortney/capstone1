"""Seed database with sample data."""

from app import db
from models import User, UserActivity


db.drop_all()
db.create_all()