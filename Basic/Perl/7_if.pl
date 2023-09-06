# 7. if문
# php 조건문과 선언 형태가 동일하다

my $abc = "abcdefghi";
my $strlen = length $abc;

if($strlen >= 4) {
    print "'", $abc, "'는 4글자 이상"."\r";
} elsif (1 <= $strlen && $strlen < 4) {
    print "'", $abc, "'는 1~3글자"."\r\n";
} else {
    print "'", $abc, "'는 1글자 이하"."\r\n";
}
