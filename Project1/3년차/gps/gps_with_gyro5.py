import ctypes  # 파이썬 extension을 사용하기 위한 모듈


path = "./gwg5.so"
lib = ctypes.cdll.LoadLibrary(path)


class Obj(ctypes.Structure) :
    _fields_ = [("nNum", ctypes.c_int),
                 ("fFloat", ctypes.c_double)]


obj = Obj()
lib.func(ctypes.byref(obj))
print(obj.nNum, obj.fFloat)

