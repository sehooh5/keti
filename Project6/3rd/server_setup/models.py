# models.py
from sqlalchemy import Column, DateTime, String
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()


class AI_uploaded(db.Model):
    __tablename__ = 'ai_uploaded'

    aid = db.Column(db.String(32), primary_key=True)
    filename = db.Column(db.String(32))
    version = db.Column(db.String(32))
    ai_class = db.Column(db.String(32))

class AI_deployed(db.Model):
    __tablename__ = 'ai_deployed'

    nid = db.Column(db.String(32), primary_key=True)
    aid = db.Column(db.String(32), primary_key=True)

class Node_info(db.Model):
    __tablename__ = 'nodes'

    nid = db.Column(db.String(32), primary_key=True)
    nip = db.Column(db.String(32), unique=True)
