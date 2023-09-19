# 14. 시스템 관리작업

use strict;
use warnings;

opendir(dirHandle, ".") or die "$!\n";
my @items = readdir(dirHandle);
closedir dirHandle;

foreach(@items) {
    next if $_ =~ /^\.\.?$/;    # . or .. 이면 skip
    next unless (-f $_);        # 디렉터리 이면 skip
    print $_, "\n";             # 파일명이면 출력
}