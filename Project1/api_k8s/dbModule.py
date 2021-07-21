# file name : dbModule.py
# pwd : /project_name/app/module/dbModule.py
 
import pymysql
 
class Database():
    def __init__(self):
        self.db= pymysql.connect(host='localhost',
                                  user='root',
                                  password='C:\Users\KETI\Desktop\git\keti\Project1\api_k8s\dbModule.py',
                                  db='sw',
                                  charset='utf8')
        self.cursor= self.db.cursor(pymysql.cursors.DictCursor)
 
    def execute(self, query, args={}):
        self.cursor.execute(query, args) 
 
    def executeOne(self, query, args={}):
        self.cursor.execute(query, args)
        row= self.cursor.fetchone()
        return row
 
    def executeAll(self, query, args={}):
        self.cursor.execute(query, args)
        row= self.cursor.fetchall()
        return row
 
    def commit():
        self.db.commit()


출처: https://kkamikoon.tistory.com/162 [컴퓨터를 다루다]