import socketio

sio = socketio.Client()


sio.connect('http://localhost:5000')

nodeport = "30000"
device_url = "rtsp://keti:keti1234@192.168.100.60:8805/videoMain"

sio.emit('nodeport', nodeport)
sio.emit('device_url', device_url)


# sio.wait() # cannot keyboard interrupt this
sio.sleep(5)
sio.disconnect()
