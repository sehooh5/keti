# Document

## 사용 된 python module

### Pickle

- [pickle document](https://docs.python.org/ko/3/library/pickle.html)

- 사용 된 함수

  - **pickle.dumps**(server.py에서 사용) : 
    - 객체 obj 의 피클된 표현을 파일에 쓰는 대신 bytes 객체로 반환 (직렬화)
  - **pickle.loads**(client.py에서 사용) : 
    - 객체의 피클 된 표현 *data*의 재구성된 객체 계층 구조를 반환 (역질렬화)
    - data 는 [바이트열류 객체](https://docs.python.org/ko/3/glossary.html#term-bytes-like-object)

- 사용 된 예시

  - server.py : 

    - **pickle.dumps**(color_frame, 0) : cv2.imencode() 에 의해 인코딩 된 frame data(color_frame) 를 직렬화

      - 직렬화 전 :

        [[137]
         [ 80]
         [ 78]
         ...
         [ 66]
         [ 96]
         [130]]

      - 직렬화 후 : 

        ............................x18\x8c1\xc8Lz\x04\x11A\x95) \x879\x1c/\x19c\xa5\xb5\xc6\xcd\x9b79\xdd\xed\x90\x84\x9c4\t\xa9!\x89\x93y\xe6\xb8\x1ei\xd3\x8e\xde;\x99\xc9\xf9\xf99\xdf}\xfd\rP\x07\x82M\xda\x14\x0f\xd9&\x00ID\x04\xb61\xc9f\x9a\x1a\x9f\xf8\xc4\'8;;\xe3\xe4\xe4\x84\xd6\x1a\xb6\x98[\'\xd3\xe4\xba\x92\xa38\x99Ox\xfb\xed\xb7\xb9w\xef\x0e\x11A\x01I\xe10c,X""\x90\x04\x04\xe1\x00\x84J\x80\x98Z\x90\x99T\x15P8\xc0N\x14\xc6\x12\x92\x18\xb9"\x02\x92\x7f*\xb0Mf\x81\x03I\xd0@\x12\xb2\xa9*\\u000a#\x1bID\x00UD\x04i\x03\xc1\xa6\xaa\xb0\x8d$$!\t;\xa9*\xaa\x8aMD`\x1b\xdbl"\x82\xaa\x02\x15\xc5C\x92(\x1e\x92\x8d~\xf2\x0b?\xe5\xef\............................

  - client.py : **pickle.loads**(frame_data, fix_imports=True, encoding="bytes") 는 반대

### Struct

- [sturct document](https://docs.python.org/3/library/struct.html)

- 사용된 함수

  - **struct.pack(format, v1, v2)**(server.py에서 사용) : 
    - 형식 문자열 *format* 에 따라 패킹 된 *v1* , *v2* ,… 값을 포함하는 **bytes 객체**를 반환
    - 인수는 형식에 <u>필요한 값과 정확히 일치해야 함</u> (예, 2s = 길이가 2 인 문자열)
  - **struct.unpack(format, 버퍼)**(client.py에서 사용) : 
    - 형식 문자열 *format* 에 따라 버퍼에서 압축을 해제
    - 결과는 정확히 하나의 항목을 포함하더라도 **튜플 객체**
    - 버퍼의 크기 (바이트)는에 반영된대로 형식에 필요한 크기와 일치해야함

- 사용 된 예시

  - server.py : 

    - **struct.pack**(">L 280s", size, text.encode()) : 

      - format : ">L 280s", '>L' = 빅 엔디안 unsigned long  //  '280s' = 280바이트 char[]

      - v1 : size, pickle 즉 직렬화된 data의 사이즈 (보통 950,000 - 단위 byte)

      - v2 : text(메타 데이터), 텍스트를 encode() 를 사용해 데이터형식(b'')으로 변환함

      - 직렬화 전 :

        [[137]
         [ 80]
         [ 78]
         ...
         [ 66]
         [ 96]
         [130]]

      - 직렬화 후 : 

        ............................x18\x8c1\xc8Lz\x04\x11A\x95) \x879\x1c/\x19c\xa5\xb5\xc6\xcd\x9b79\xdd\xed\x90\x84\x9c4\t\xa9!\x89\x93y\xe6\xb8\x1ei\xd3\x8e\xde;\x99\xc9\xf9\xf99\xdf}\xfd\rP\x07\x82M\xda\x14\x0f\xd9&\x00ID\x04\xb61\xc9f\x9a\x1a\x9f\xf8\xc4\'8;;\xe3\xe4\xe4\x84\xd6\x1a\xb6\x98[\'\xd3\xe4\xba\x92\xa38\x99Ox\xfb\xed\xb7\xb9w\xef\x0e\x11A\x01I\xe10c,X""\x90\x04\x04\xe1\x00\x84J\x80\x98Z\x90\x99T\x15P8\xc0N\x14\xc6\x12\x92\x18\xb9"\x02\x92\x7f*\xb0Mf\x81\x03I\xd0@\x12\xb2\xa9*\\u000a#\x1bID\x00UD\x04i\x03\xc1\xa6\xaa\xb0\x8d$$!\t;\xa9*\xaa\x8aMD`\x1b\xdbl"\x82\xaa\x02\x15\xc5C\x92(\x1e\x92\x8d~\xf2\x0b?\xe5\xef\............................

  - client.py : **struct.unpack**(frame_data, fix_imports=True, encoding="bytes") 는 반대