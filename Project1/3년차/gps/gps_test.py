import serial

ser = serial.Serial(port='/dev/serial0', baudrate=9600, parity=serial.PARITY_NONE,
                    stopbits=serial.STOPBITS_ONE, bytesize=serial.EIGHTBITS)
# if ser.readable():
#     res = ser.readline()
#     print(res.decode()[:len(res) - 1])

buffer=""
while True:
   oneByte = ser.read(1)
   if oneByte == b"\r":    #byte단위로 read, 구분자 '\r'
        break
   else:
        data=oneByte.hex()
        print(data)
        buffer += oneByte.decode('cp949')

print (buffer.strip())