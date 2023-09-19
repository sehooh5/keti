# 13. 시스템 콜
# 시스템 콜을 통해 프로그램을 엮어주는 '글루 코드' 작성 가능

# 시스템 콜으로 외부 명령어 실행
my $rc = system "perl", "1_perl.pl";
print $rc; # 0 => 프로세스의 status word를 출력

my $result = qx("ping localhost"); # 명령어 실행 결과를 변수에 저장
print $result;