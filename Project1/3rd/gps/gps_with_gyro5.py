import ctypes  # 파이썬 extension을 사용하기 위한 모듈


path = "./gwg5.so"
c_module = ctypes.cdll.LoadLibrary(path) # cpp 로 생성한 모듈(.so)을 ctypes 모듈로 불러오기

# .so 에 정의된 구조체와 같은 구조체 만들기
class STRUCT(ctypes.Structure) :
    _fields_ = [("nNum", ctypes.c_int),
                 ("fFloat", ctypes.c_double)]


str = STRUCT() # 만들어진 구조체 변수선언
c_module.strToPython(ctypes.byref(str)) # ctypes의 byref 에 ctypes.Structure 객체를를 넣어서 .so 모듈의 함수에 전달
print(str.nNum, str.fFloat) # 포인터로 반환된 구조체의 변수 불러오기


# ctypes.byref(obj[, offset]) 설명 :
# obj에 대한 경량 포인터를 반환합니다. obj는 ctypes 형의 인스턴스여야 합니다.

# ctypes.pointer(obj) 로 대체 가능
