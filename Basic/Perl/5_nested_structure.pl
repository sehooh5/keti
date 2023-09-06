# 5. 중첩 구조 처리
# 배열 특정 인덱스에 다른 배열을 할당할 때,
# 스칼라 변수로 취급되어 배열 요소 개수가 할당된다.

my @outer = ("Mon", "Tue", "Wed", "Thu", undef, "Fri");
my @inner = ("Sat", "Sun");

$outer[4] = @inner; # @inner는 scala 변수로 취급되어 2가 할당됨
print $outer[4]; # "2"

$outer[4] = inner[0]; # @inner 의 0번 변수가 할당됨
print $outer[4]; # "Sat"
