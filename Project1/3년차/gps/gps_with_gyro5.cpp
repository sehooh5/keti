#define EXPORT

// Structure(구조체)에 담을 변수 선언
int a;
double b;

// 구조체 선언 - 여기서는 int 와 double 두 개로 이루어진 구조체
struct Struct {
	int num;
	double f;
};

extern "C" {
    // return 값 없이 Pointer로 구조체를 반환하는 함수 정의 및 EXPORT
    // 함수의 파라미터도 void 로 받으며 Pointer 로 받는다
    EXPORT void strToPython(void* st) {
        // 변수 입력
        a = 1991;
        b = 2.8;

        // 위에서 선언한 구조체를 변수로 만들고 위에서 입력된 변수들을 구조체에 담는다
        Struct temp = {a,b};
        // 포인터 지정하는 부분
        // 함수의 포인트 파라미터로 받은 void* st를 선언한 구조체인 Struct*로 형변환 후 *포인터..?
        *((Struct*)st) = temp;
    }

}







