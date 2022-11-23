import json



def read_file():
    f = open("test.txt", "r")
    line = f.read()
    # f.close
    return line

while True:
    i = 0;
    data = read_file()
    print(data)
    if i == 1:
        break;
