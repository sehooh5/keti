# models.py
from sqlalchemy import Column, DateTime, String
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class SW_up(db.Model):
    __tablename__ = 'software_up'
    
    sid = db.Column(db.String(32), primary_key=True)
    name = db.Column(db.String(32))
    fname = db.Column(db.String(128))
    copyright = db.Column(db.String(128))
    type = db.Column(db.String(128))
    description = db.Column(db.String(128))
