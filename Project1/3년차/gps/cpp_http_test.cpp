#include <stdio.h>
#include <curl/curl.h>

#include <iostream>
#include "json/json.h"

std::string str;

{
    Json::Value root;
    root["id"] = "SH";
    root["name"] = "SEHO";
    root["age"] = 10000;
    root["hasCar"] = false;

    Json::StyledWriter writer;
    str = writer.srite(root);
    std::cout << str << std::ednl << std::endl;
}



int main(void)
{
  CURL *curl;
  CURLcode res;

  /* In windows, this will init the winsock stuff */
  curl_global_init(CURL_GLOBAL_ALL); // 이 옵션은 thread 메모리 공유에 안전하지 않다. 나는 주석처리함

  /* get a curl handle */
  curl = curl_easy_init();

  struct curl_slist *list = NULL;

  if(curl) {
    curl_easy_setopt(curl, CURLOPT_URL, "http://123.214.186.162:8088/test"); //webserver ip 주소와 포트번호, flask 대상 router

    list = curl_slist_append(list, "Content-Type: application/json"); // content-type 정의 내용 list에 저장
    curl_easy_setopt(curl, CURLOPT_HTTPHEADER, list); // content-type 설정

    curl_easy_setopt(curl, CURLOPT_SSL_VERIFYPEER, 1L); // 값을 false 하면 에러가 떠서 공식 문서 참고함
    curl_easy_setopt(curl, CURLOPT_SSL_VERIFYHOST, 1L); // 값을 false 하면 에러가 떠서 공식 문서 참고함

    curl_easy_setopt(curl, CURLOPT_POST, 1L); //POST option
    curl_easy_setopt(curl, CURLOPT_POSTFIELDS,"data"); //string의 data라는 내용을 전송 할것이다

    /* Perform the request, res will get the return code */
    res = curl_easy_perform(curl); // curl 실행 res는 curl 실행후 응답내용이
    curl_slist_free_all(list); // CURLOPT_HTTPHEADER 와 세트

    /* Check for errors */
    if(res != CURLE_OK)
      fprintf(stderr, "curl_easy_perform() failed: %s\n",curl_easy_strerror(res));

    /* always cleanup */
    curl_easy_cleanup(curl); // curl_easy_init 과 세트
  }
  curl_global_cleanup(); // curl_global_init 과 세트
  return 0;

}
