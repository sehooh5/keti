# 3. 배열 타입  - python 의 list 형태. 변수의 요소는 숫자, 문자열이 올 수 있다.
# 배열 변수명 앞에 @ 를 붙여 선언한다.

my @array = (
    "one",
    "two",
    "three", # trailing comma용
);
print "배열요소는 ".(scalar @array)."개\r\n";
print "배열요소는 @array\r\n";
print $array[0];
print $array[1];print $array[2];