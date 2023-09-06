# 2. Perl 에서 일반변수, Scala 변수
# 일반 변수의 타입은 undef, number(int, float), string / Perl은 Boolean 타입이 없다.
# Scala의 변수는 우리가 흔히 생각하는 변수와 개념으로 사용하는 변수(var)와 변하지 않는 값을 의미하는 값(val)이 있다. 그중에서 scala는 값(val)사용을 지향하는 편이다.
# 컴파일러가 자료형을 추론하여 컴파일 단계에서 정해주기 때문에 자료형을 생략해도 scala 컴파일러가 대입하는 값을 보고 자료형을 정해준다.

my $undef = undef;
print $undef; #빈 문자열 (" ")을 출력함

my $undef2; # implicit undef 선언
print $undef2;

my $num = 100;
print $num; # "100"을 출력

my $stringg = "hello\r\n";
print $stringg; # "hello"를 출력