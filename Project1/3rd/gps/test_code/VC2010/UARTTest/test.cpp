#include <iostream>
#include <fstream>
#include "json.h"
#pragma  comment(lib,"jsoncpp\\lib\\lib_json.lib")
#pragma warning(disable: 4996)                    //error C4996 뜨는 경우
using namespace std;

int main()
{
	string str;
	Json::Value root;
	root["name"] = "KKK";
	root["age"] = 12;
	root["address"] = "kor";
	root["gfriend"] = true;

	Json::Value family;
	family.append("mother");
	family.append("father");
	family.append("brother");
	root["family"] = family;

	Json::StyledWriter writer;
	str = writer.write(root);
	cout << str << endl ;

	std::ofstream ost("test.json");
	ost << str;

	getchar();
	return 0;
}