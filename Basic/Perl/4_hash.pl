# 4. 해쉬 타입 - Python 의 Dictionary 타입.
# 해쉬 변수명의 앞에 % 를 붙여 선언한다.

my %hashValues = (
    "1" => "One",
    "2" => "Two",
    "3" => "three", # trailing comma용
);
print $hashValues{"1"};
print $hashValues{"2"};
print $hashValues{"3"};