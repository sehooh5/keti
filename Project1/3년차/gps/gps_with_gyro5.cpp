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




struct St {
	int x;
	double f;
};

extern "C" {
    EXPORT void func(void* st) {
        St temp = {1, 3.14};
        *((St*)st) = temp;
    }

}







