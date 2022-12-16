import ctypes


path = "./gwg4.so"
c_module = ctypes.cdll.LoadLibrary(path)
print("시작!!")

class STRUCT(ctypes.Structure) :
    _fields_ = [("mi", ctypes.c_int),
                ("ss", ctypes.c_int),
                ("ms", ctypes.c_int)]


str = STRUCT()
c_module.process(ctypes.byref(str))
print(str.mi)
# print(str.mi, str.ss, str.ms, str.ax, str.ay, str.az)