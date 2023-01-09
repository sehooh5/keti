# sqlalchemy python 내부에서 사용가능
from sqlalchemy import create_engine 
from sqlalchemy.orm import scoped_session, sessionmaker 
from sqlalchemy.ext.declarative import declarative_base
import pymysql
pymysql.install_as_MySQLdb()

# DB로 접속 가능하게 engine 생성
engine =create_engine('sqlite:///:memory', echo=True)
# session_maker 접속이 끝나더라도 계속 연결상태 유지시키기위해
db_session = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))

Base = declarative_base() 
Base.query = db_session.query_property()

def init_db(): 
    import models 
    Base.metadata.create_all(engine)