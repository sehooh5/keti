

import ctypes  # 파이썬 extension을 사용하기 위한 모듈


#######################################
path = "./gpg5.so"
c = ctypes.cdll.LoadLibrary(path)

class POINT(ctypes.Structure):
    _fields_ = [
        ("a", ctypes.c_int),
        ("b", ctypes.c_int),
        ("c", ctypes.c_float)
    ]
point = POINT()
list = c.process(point)
print(list)
# point = POINT(c.one.a, c.one.b, c.one.c)
#
# print(point.a, point.a, point.a)



# 가장 기본되는 구조체
# class POINT(ctypes.Structure):
#     _fields_ = [
#         ("a", ctypes.c_int),
#         ("b", ctypes.c_int)
#     ]
#
# point = POINT(10,20)
# print(point.a, point.b)