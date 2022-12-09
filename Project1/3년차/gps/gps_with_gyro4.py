# import sys
# import json
# import time
# import requests
#
#
# url = "http://123.214.186.162:8088"
#
# def read_file():
#     f = open("test.txt", "r")
#     line = f.read()
#     f.close
#
#     return line
#
# ## 무한 루프
# while True:
#     i = 0;
#     data = read_file()
#     arg = sys.argv
#
#     if len(arg) > 1 :
#         res = requests.post(f'{url}/gwg_save', json=data)
#     else:
#         res = requests.post(f'{url}/gwg', json=data)
#
#     print(res)
#     time.sleep(1)
#     if i == 1:
#         break;

import ctypes  # 파이썬 extension을 사용하기 위한 모듈
import platform  # 파이썬 아키텍처를 확인하기 위한 모듈

path = "./libc_module.so"
c_module = ctypes.cdll.LoadLibrary(path)

c_module.main()
# c_tuple = c_module.res_num()
# print(c_tuple)
