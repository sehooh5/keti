import ctypes


path = "./gwg4.so"
c_module = ctypes.cdll.LoadLibrary(path)

class STRUCT(ctypes.Structure) :
    _fields_ = [("mi", ctypes.c_int),
                ("ss", ctypes.c_int),
                ("ms", ctypes.c_int),
                ("ax", ctypes.c_float),
                ("ay", ctypes.c_float),
                ("az", ctypes.c_float)]


str = STRUCT()
c_module.process(ctypes.byref(str))
print(str.mi, str.ss, str.ms, str.ax, str.ay, str.az)