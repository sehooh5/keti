# models.py
from sqlalchemy import Column, DateTime, String
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class SW_up(db.Model):
    __tablename__ = 'software_up'
    
    sid = db.Column(db.String(32), primary_key=True)
    name = db.Column(db.String(32))
    fname = db.Column(db.String(128))
    copyright = db.Column(db.String(128))
    type = db.Column(db.String(128))
    description = db.Column(db.String(128))
    datetime = db.Column(db.DateTime, default = datetime.utcnow())

class Server(db.Model):
    __tablename__ = 'server'
    
    sid = db.Column(db.String(32), primary_key=True)

class Server_SW(db.Model):
    __tablename__ = 'server_sw'
    
    sid = db.Column(db.String(32), primary_key=True)
    wid = db.Column(db.String(32), primary_key=True)
    serviceport = db.Column(db.String(32))
    nodeport = db.Column(db.String(32))
    targetport = db.Column(db.String(32))
    
