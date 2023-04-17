#include “stdafx.h”
#include “includePython.h”
#include <iostream>

using namespace std;
int main()
{

PyObject *pName, *pModule, *pFunc, *pValue;

PyObject* pArgs;
double dVal1 = 1;
double dVal2 = 2;
Py_Initialize();
//testFile.py 파일이 있는 위치를 정의 한다
PyRun_SimpleString(“import sys”);
PyRun_SimpleString(“sys.path.append(r’D:\\TASK_Daily\\Job20201105\\usubp\\console_application\\python_via_main\\x64\\Debug’)”);
pArgs = PyTuple_New(2);
PyTuple_SetItem(pArgs, 0, PyLong_FromLong(dVal1));
PyTuple_SetItem(pArgs, 1, PyLong_FromLong(dVal2));
pName = PyUnicode_FromString(“testFile”); // testFile.py를 PyObject로 생성한다.
pModule = PyImport_Import(pName); // 생성한 PyObject pName을 import한다.
pFunc = PyObject_GetAttrString(pModule, “plus”); // 실행할 함수인 plus를 PyObject에 전달한다.
pValue = PyObject_CallObject(pFunc, pArgs); // pFunc에 매개변수를 전달해서 실행한다.
Py_Finalize();
double dVal3 = PyLong_AsLong(pValue); // pFunc의 결과를 변수에 할당한다
std::cout << dVal3 << endl; // 변수값을 출력한다

return 0;

}