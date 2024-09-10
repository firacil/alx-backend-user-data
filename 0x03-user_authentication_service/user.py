#!/usr/bin/env python3
"""module to declare sqlalchemy model named user"""

from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()


class User(db.Model):
    """class User model of db called users"""
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(250), unique=True, nullable=False)
    hashed_password = db.Column(db.String(250), nullable=False)
    session_id = db.Column(db.String(250), nullable=True)
    reset_token = db.Column(db.String(250), nullable=True)
