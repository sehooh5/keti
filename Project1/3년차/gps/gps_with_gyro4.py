import ctypes


path = "./gwg4.so"
c_module = ctypes.cdll.LoadLibrary(path)

class STRUCT(ctypes.Structure) :
    _fields_ = [("mi", ctypes.c_uint),
                ("ss", ctypes.c_uint),
                ("ms", ctypes.c_uint)]


str = STRUCT()
c_module.process(ctypes.byref(str))
print("프린트!!!!!")
print(str.mi)
# print(str.mi, str.ss, str.ms, str.ax, str.ay, str.az)