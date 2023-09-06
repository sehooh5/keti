# 6. 참조
# 일반 변수에 다른변수를 할당 받아 참조 변수 역할을 할 수 있다.
# C 포인터처럼 참조 주소를 출력하거나 참조 값 출력이 가능하다.

my $hello = "Hello";
my $helloRef = \$hello;

print $hello."\r\n";
print $helloRef."\r\n";
print ${ $helloRef }."\r\n";
print $$helloRef;
