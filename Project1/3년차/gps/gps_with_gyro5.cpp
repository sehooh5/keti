#include<stdio.h>
#include<stdlib.h>
#include<fcntl.h>
#include<unistd.h>
#include<assert.h>
#include<termios.h>
#include<string.h>
#include<sys/time.h>
#include<time.h>
#include<sys/types.h>
#include<errno.h>

#include<iostream>
#include<fstream>

/* c++ to python 추가내용 */
#define EXPORT
#include <vector>
#include <numeric>
#include <tuple>
/* end */




extern "C"
{
    EXPORT typedef struct {
        int a;
        int b;
        float c;
//        unsigned char* pBuffer;
    }  POINT;

    EXPORT POINT process(POINT p){
        p = {101,20,3.14};

        return p;
    }
//    struct POINT input_p(void);
//    void display_p(struct POINT d);
//
//    EXPORT int main(void){
//        POINT d;
//        d = input_p();
//        display_p(d);
//        return 0;
//    }
//
//    void display_p(struct POINT s){
//        printf("a %d", s.a);
//        printf("b %d", s.b);
//        printf("c %f", s.c);
//    }
//
//    struct POINT input_p(void){
//        POINT s;
//        s.a = 10;
//        s.b = 20;
//        s.c = 3.14;
//        return s;
//    }


//    POINT main(void)


//    tuple<int, int, float> t1;
//    EXPORT tuple<int,int,float> getTuple(){
//        int a = 10;
//        int b = 20;
//        float c = 3.14;
//        return make_tuple(a,b,c);
//    }

}




