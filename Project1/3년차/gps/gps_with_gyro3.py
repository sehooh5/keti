import json



def read_file():
    f = open("test.txt", "r")
    line = f.read()
    # f.close
    return line

while True:
    data = read_file()
    print(data)
    break;
