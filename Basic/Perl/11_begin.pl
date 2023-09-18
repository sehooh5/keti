# 11. BEGIN
# BEGIN 블록은 파싱되는 순간 바로 실행된다

use strict;
use warnings;

print "하나";

BEGIN {
    print "둘";
}

print "셋";
# 둘하나셋