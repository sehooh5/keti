

/* c++ to python 추가내용 */
#define EXPORT


int a;
double b;

struct St {
	int x;
	double f;
};

extern "C" {
    EXPORT void func(void* st) {
        a = 1991;
        b = 2.8;
        St temp = {a,b};
        *((St*)st) = temp;
    }

}







