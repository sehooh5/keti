import socket

print("Host Name ",socket.gethostname())

print("IP Address(Internal) : ",socket.gethostbyname(socket.gethostname()))

print("IP Address(External) : ",socket.gethostbyname(socket.getfqdn()))