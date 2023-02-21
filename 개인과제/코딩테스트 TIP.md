# 코딩테스트 TIP

- 리스트 내 갯수 세기

  - array.count(n)

- 문자열은 곱셈이 가능하다

  - string*4 = stringstringstringstring

- 소수점을 버리고 정수 만들기

  - int(float)

- 알파벳 -> 아스키코드

  - ord("a") = 97
  - ord("A") = 65

- 숫자 -> 알파벳

  - chr(97) = "a"

- 배열 올림차순

  - [list 변수].sort() // 기존 list를 변경
  - [sorted_list 변수] = sorted([list 변수]) // 기존 list 변경 없이 새롭게 

- 문자열 잘라서 리스트로 만들기

  - [문자열 변수].split('[자를 문자]')

- 2차원 배열을 만들때

  - array = []을 설정해주고 그 안에 다른 array2 배열을 append 해주면 된다

- 자연수 주어졌을 때 약수 구하는 방법 

  ```python
  def solution(n):
      factors = []
      for i in range(1, n+1):
          if n % i == 0:
              factors.append(i)
      return factors
  ```

- 배열에서 값 삭제

  - array.remove(값)

- 소수 판별법

  ```python
  def is_prime_number(x):
      # 2부터 (x - 1)까지의 모든 수를 확인하며
      for i in range(2, x):
          # x가 해당 수로 나누어떨어진다면
          if x % i == 0:
              return False # 소수가 아님
      return True # 소수임
  ```

- sort() 와 sorted()

  - 리스트.sort()는 본체 리스트를 정렬해서 변환
  - sorted(리스트)는 본체 리스트는 그냥 두고, 정렬한 새로운 리스트 반환
    - 변수로 문자열을 넣어주면 각 문자를 배열로 정렬해서 리스트로 반환한다

- str.isalpha(문자) / str.isdigit(문자)

  - str.isalpha(문자) : 문자가 알파벳인지 확인
  - str.isdigit(문자) : 문자가 숫자인지 확인

- '0b10111' 문자열을 정수로

  - int('0b10111',2)
    - 2번째 인자는 2진수

- 정수를 이진수로

  - bin(정수)

- 매개변수로 받은 문자열 expression(식)을 실행시켜주는 함수

  - eval("1+2-3")

- 직사각형의 넓이

  - 최대값과 최소값의 x,y 차이를 곱해주면 된다

- enumerate 함수 with for

  - for i, num in enumerate(list):
    - 0, A / 1,B

- 연속하는 숫자 list 만들기

  - list(range(1,10))

- 두 개의 리스트 간 중복요소 찾기 

  - **list(set(**리스트1**).intersection(**리스트2**))**