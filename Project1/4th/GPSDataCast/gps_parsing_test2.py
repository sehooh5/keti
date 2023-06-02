import serial
import time

num = sys.argv[1]

conn = sqlite3.connect(f"gps_0{num}.db", isolation_level=None, check_same_thread=False)
c = conn.cursor()

c.execute("SELECT COUNT(*) FROM gps_raw_data")
for row in c:
    num = row[0]


def parse_data(data):
    s_data = [0] * 9
    c_temp = 0

    for i in range(10):
        c_temp += data[i]

    if data[0] != 0x55 or (data[1] & 0x50) != 0x50 or c_temp != data[10]:
        print("Error:", hex(data[0]), hex(data[1]))
        return

    s_data = [int.from_bytes(data[i:i+2], byteorder='little', signed=True) for i in range(2, 10)]

    data_type = data[1]
    if data_type == 0x51:
        a = [float(x) for x in s_data]
        print("Acc:", a)
    elif data_type == 0x52:
        w = [float(x) for x in s_data]
        print("Gyro:", w)
    elif data_type == 0x53:
        Angle = [float(x) for x in s_data]
        print("Angle:", Angle)
    elif data_type == 0x54:
        h = [float(x) for x in s_data]
        print("Magnetic:", h)
    elif data_type == 0x56:
        ph = [float(x) for x in s_data]
        print("Pressure:", ph)
    elif data_type == 0x57:
        gps = [float(x) for x in s_data]
        print("GPS:", gps)
    elif data_type == 0x58:
        s = [float(x) for x in s_data]
        print("Speed:", s)
    elif data_type == 0x59:
        q = [float(x) for x in s_data]
        print("Quaternion:", q)
    elif data_type == 0x5A:
        sp = [float(x) for x in s_data]
        print("Satellite Positioning:", sp)

def main():

    while True:
        for num in range(1, num+1):
        if num == 1:
            print("데이터 초기화")
        c.execute(f"SELECT * FROM gps_raw_data WHERE ROWID={num}")
        for row in c:
            print(f"로우 데이터 {row[2]}")

        # 로우데이터 읽은 후 여기서 잘 처리해줘야할듯
        if ser.inWaiting() > 10: # 수신 버퍼의 바이트 수를 반환
            data = ser.read(11)
            parse_data(data)
        time.sleep(0.001)

    ser.close()

if __name__ == "__main__":
    main()
