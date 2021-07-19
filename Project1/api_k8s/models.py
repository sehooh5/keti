# models.py
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Software(db.Model):
    __tablename__ = 'software'
    
    sid = db.Column(db.String(16), primary_key=True)
    name = db.Column(db.String(32))
    fname = db.Column(db.String(128))
    copyright = db.Column(db.String(128))
    type = db.Column(db.String(128))
    description = db.Column(db.String(128))
    datetime = db.Column(db.DateTime)
