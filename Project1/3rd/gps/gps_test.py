import serial

ser = serial.Serial(port='/dev/ttyUSB2', baudrate=9600, parity=serial.PARITY_NONE,
                    stopbits=serial.STOPBITS_ONE, bytesize=serial.EIGHTBITS)
# if ser.readable():
#     res = ser.readline()
#     print(res.decode('utf-16')[:len(res) - 1])

buffer=""
while True:
   oneByte = ser.read(2)
   if oneByte == b"\r":    #byte단위로 read, 구분자 '\r'
        pass
   else:
        print(oneByte)
        # buffer += oneByte.decode()

print (buffer.strip())