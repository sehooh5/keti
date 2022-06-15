import sqlite3
import sys

# DB 생성 (오토 커밋)
conn = sqlite3.connect("test.db", isolation_level=None)
# 커서 획득
c = conn.cursor()

# device ID 마다 table 만들어 주기 위함
table = sys.argv[1]

# 테이블 존재 확인
c.execute('select name from sqlite_master where type="table" and name="d11"')
if c.fetchone() == None:
    print('테이블 없음')




# 데이터 불러오기
c.execute(f"SELECT max(id) FROM {table}")
# print("id 중 가장 큰 수", c.fetchone()[0])
max_id = c.fetchone()[0]

c.execute(f"SELECT min(id) FROM {table}")
print("id 중 가장 작은 수", c.fetchone()[0])

# 테이블 생성 (데이터 타입은 TEST, NUMERIC, INTEGER, REAL, BLOB 등)
c.execute(f"CREATE TABLE IF NOT EXISTS {table} \
    (id integer PRIMARY KEY, msg text)")

#데이터 삽입 방법 1
# c.execute(f"INSERT INTO {table} \
#     VALUES(?,?)", (4, 'msg from sender'))


# print(c.fetchone())
# print(c.fetchall()[0][0])
