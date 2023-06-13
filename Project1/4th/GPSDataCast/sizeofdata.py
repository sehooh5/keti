import sqlite3

def get_data_size(db_file, table_name, column_name):
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()

    # 데이터 크기 쿼리 실행
    query = f"SELECT LENGTH({column_name}) FROM {table_name}"
    cursor.execute(query)
    data_size = cursor.fetchone()[1]

    conn.close()
    return data_size

# 예시 사용
db_file = "gps_02.db"
table_name = "gps_raw_data"
column_name = "raw_data"

size = get_data_size(db_file, table_name, column_name)
print(f"데이터 크기: {size} bytes")