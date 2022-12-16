import ctypes  # 파이썬 extension을 사용하기 위한 모듈


path = "./gwg5.so"
c_module = ctypes.cdll.LoadLibrary(path) # cpp 로 생성한 모듈(.so)을 ctypes 모듈로 불러오기

# .so 에 정의된 구조체와 같은 구조체 만들기
class STRUCT(ctypes.Structure) :
    _fields_ = [("nNum", ctypes.c_int),
                 ("fFloat", ctypes.c_double)]


str = STRUCT() # 만들어진 구조체 변수선언
c_module.strToPython(ctypes.byref(str)) # ctypes의 byref 에 구조체를 넣어서 .so 모듈의 함수에 전달
print(str.nNum, str.fFloat) # 포인터로 반환된 구조체의 변수 불러오기

