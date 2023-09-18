# 12. 객체지향 프로그래밍
# Perl에서 클래스 역할을 하는 것은 Package 이다.
# 네임 스페이스 역할을 하면서 서브 메서드를 선언할 수 있다.

# Package 초기화될 때 생성자(constructor)는 다음과 같은 형태로 선언한다.
#sub new {
#    my $this = {};  # 익명 해쉬를 생선하고 자신(Hello 패키지)을 가르키게함
#
#    bless $this;    # Hello 패키지와 연결
#
#    return $this;   # Hello 패키지를 참조
#};


# Package 선언
package Hello;

use strict;
use warnings;

# 생성자
sub new{
    my ($class, %args) = @_;
    return bless { %args }, $class;
};

# Hello 클래스의 매서드
sub helloWorld {
    my ($self) = @;
    print $self->{data1}." ";
    print $self->{data2};
};

my $helloObject = Hello->new( data1 => 'hello',
                        data2 => 'world');
$helloObject->hellowWorld();

