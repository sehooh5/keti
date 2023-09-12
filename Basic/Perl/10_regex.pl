# 10. regex - 정규식 매칭
# match 동작을 수행하기 위해 “=~ m/“를 사용했다. replace 동작 수행은 “=~ s/“를 사용한다.
# ^ 문자열시작 / $ 문자열 끝 / . 새로운 라인을 제외한 모든 문자 / * 0번 이상 매칭
# + 1번 이상 매칭 / ? 0 또는 1번 매칭 / | 대체 / () 그룹핑 / [] 문자열 셋 / {} 반복 / \ 특수문자 앞에 둠

# Match 처리
my $string = "Hello world";
if($string =~ m/(\w+)\s+(\w+)/) { # success
	print "success";
}

# Replace 처리
my $string = "One Two Three";
$string =~ s/Two/2/;
print $string; # "One 2 Three"