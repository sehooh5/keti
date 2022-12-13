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
import time

#######################################
path = "./libc_module.so"
c_module = ctypes.cdll.LoadLibrary(path)


# # 이 코드만 실행시키면 원래 버전과 같음
c_module.process()

# while 1:
#     f = c_module.sendData
#     f.argtypes = None
#     f.restype = ctypes.c_char_p
#     res = f()
#     print("Print!!", res)
########################################
## out 파라메터로 포인터를 사용할때
# process = c_module.process
# process.argtype = (ctypes.POINTER(ctypes.c_float))
# process.restype = None
# outparam = ctypes.c_float()
# process(outparam)
# print(outparam.value)



# f = c_module.process
# f.argtypes = None
# f.restype = ctypes.c_float
# res = f()
# print(res)

# c_module.main()
# c = c_module.res_num
# c.argtype = None
# c.restype = ctypes.c_float
# res = c()
# print(res)

# f = c_module.res_num
# f.argtypes = None
# f.restype = ctypes.c_float
# res = f()
# print(res)