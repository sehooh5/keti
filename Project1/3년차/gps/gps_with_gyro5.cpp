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
    typedef struct EXPORT POINT{
        int a;
        int b;
        float c;
    };

    POINT one = {10,20,3.14};

}




