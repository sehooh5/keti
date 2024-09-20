from sqlalchemy import Column, String, Integer, Boolean, DateTime, ForeignKey, Table
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func
from flask_sqlalchemy import SQLAlchemy
from werkzeug.utils import secure_filename
from PIL import Image as PImage
from io import BytesIO
import os

Base = declarative_base()
db = SQLAlchemy()

category_tag_table = Table('category_tag', Base.metadata,
                           Column('category_id', Integer, ForeignKey('category.id')),
                           Column('tag_id', Integer, ForeignKey('tag.id'))
                           )

user_follow_table = Table('user_follow', Base.metadata,
                          Column('follower_id', Integer, ForeignKey('extend_user.id')),
                          Column('following_id', Integer, ForeignKey('extend_user.id'))
                          )


class Tag(Base):
    __tablename__ = 'tag'
    id = Column(Integer, primary_key=True)
    name = Column(String(20), unique=True)
    section = Column(String(20), nullable=True)

    def __str__(self):
        return self.name


class Category(Base):
    __tablename__ = 'category'
    id = Column(Integer, primary_key=True)
    name = Column(String(20), unique=True)
    image = Column(String, nullable=True)
    tags = relationship('Tag', secondary=category_tag_table, back_populates='categories')
    order = Column(Integer, default=99)

    def __str__(self):
        return self.name


class WithdrawUser(Base):
    __tablename__ = 'withdraw_user'
    id = Column(Integer, primary_key=True)
    old_id = Column(Integer)
    username = Column(String(50))
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, onupdate=func.now())


class ExtendUser(Base):
    __tablename__ = 'extend_user'
    id = Column(Integer, primary_key=True)
    name = Column(String(20), default='')
    phone_number = Column(String(13), unique=True, nullable=True)
    username = Column(String(50), unique=True)
    url = Column(String(500), default='', nullable=True)
    description = Column(String(1000), default='', nullable=True)
    nickname = Column(String(20), unique=True, nullable=True)
    email = Column(String(120), unique=True, nullable=True)
    profile_image = Column(String, nullable=True)
    followers = relationship('ExtendUser', secondary=user_follow_table,
                             primaryjoin=id == user_follow_table.c.follower_id,
                             secondaryjoin=id == user_follow_table.c.following_id,
                             backref='followings')
    agree_rule = Column(Boolean, default=True)
    agree_marketing = Column(Boolean, default=False)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, onupdate=func.now())

    def __str__(self):
        return self.username


class VerificationCode(Base):
    __tablename__ = 'verification_code'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('extend_user.id'))
    code = Column(String(6))
    created_at = Column(DateTime, default=func.now())
    verified = Column(Boolean, default=False)
    auth_hash = Column(String(39), nullable=True)
    is_valid = Column(Boolean, default=True)


class Following(Base):
    __tablename__ = 'following'
    id = Column(Integer, primary_key=True)
    following_user_id = Column(Integer, ForeignKey('extend_user.id'))
    followed_user_id = Column(Integer, ForeignKey('extend_user.id'))

    def __str__(self):
        return f"{self.following_user} -> {self.followed_user}"

# 나머지 모델들 (Image, Content, Like 등)은 동일한 방식으로 SQLAlchemy로 변환 가능
