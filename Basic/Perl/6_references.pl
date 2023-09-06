# 6. 참조
# 일반 변수에 다른변수를 할당 받아 참조 변수 역할을 할 수 있다.
# C 포인터처럼 참조 주소를 출력하거나 참조 값 출력이 가능하다.

my $hello = "Hello";
my $helloRef = \$hello; # 참조하는 방법 \

print $hello."\r\n";

print $helloRef."\r\n"; # 참조 주소 출력
print ${ $helloRef }."\r\n"; # 참조하는 값 출력하는방법 1
print $$helloRef."\r\n"; # 참조하는 값 출력하는방법 2
