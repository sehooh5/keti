import sqlite3
import sys

# DB 생성 (오토 커밋)
conn = sqlite3.connect("test1.db", isolation_level=None)

# 커서 획득
c = conn.cursor()

## sys 이용해 변수 삽입(나중에 수정할 부분)
# 첫번째 변수 table name
t_name = sys.argv[1]
act = sys.argv[2]
id = sys.argv[3]
ip = sys.argv[4]

# device 테이블이 없는지 확인
c.execute(f'select name from sqlite_master where type="table" and name="{t_name}"')
t_exist = c.fetchone()
# device 테이블이 없으면 테이블 생성
if t_exist == None:
    c.execute(f"CREATE TABLE IF NOT EXISTS {t_name} \
                    (id text PRIMARY KEY, type text, ip text)")

# 1. 데이터 삽입
if act == "insert":
    c.execute(f"INSERT INTO {t_name} \
        VALUES('{id}', '{t_name}', '{ip}')")
# 2. 데이터 찾기
elif act == "findall":
    c.execute(f"SELECT * FROM {t_name}")
    for row in c.fetchall(): # 전체 출력
        print(row)
# 3. 데이터 조회(필터링)
elif act == "find":
    c.execute(f"SELECT * FROM {t_name} WHERE id='{id}'")
    print(c.fetchone())
# 4. 데이터 수정하기 -- ## 나중에 수정해야함
elif act == "update":
    c.execute(f"UPDATE {t_name} SET type=? WHERE id=?", (f're_{t_name}', id))
# 5. 데이터 삭제하기
elif act == "remove":
    c.execute(f"DELETE FROM {t_name} WHERE id='{id}'")

# db commit
conn.commit()

# db 연결 해제
conn.close()