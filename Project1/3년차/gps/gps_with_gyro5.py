

import ctypes  # 파이썬 extension을 사용하기 위한 모듈


#######################################


path = "./gwg5.so"
lib = ctypes.cdll.LoadLibrary(path)


class Obj(ctypes.Structure) :
    _fields_ = [("nNum", ctypes.c_int),
                 ("fFloat", ctypes.c_double)]


obj = Obj()
lib.func(ctypes.byref(obj))


# ### Pointer 전달해서 받은 값
# sub = c.sub
# sub.argtypes = (ctypes.c_double, ctypes.POINTER(ctypes.c_double))
# sub.restype = None
# outparam = ctypes.c_double()
#
# sub(0, outparam)
# print(outparam.value)
#
#
#
# class str(ctypes.Structure):
#     _fields_ = [
#         ("a", ctypes.POINTER(ctypes.c_int)),
#         ("b", ctypes.POINTER(ctypes.c_int)),
#         ("c", ctypes.POINTER(ctypes.c_float))
#         # ("p", ctypes.POINTER(c.c_ubyte))
#     ]
#
# res = c.process
# res.argtypes = ctypes.POINTER(str),
# res.restype = None
#
# s = str(0, ctypes.c_int, ctypes.c_int, ctypes.c_float)
# result = res(s)
# print(result)






# point = POINT()
# list = c.process(point)
# print(str(list.a))


# tuple = c.getTuple()
# print(tuple)
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