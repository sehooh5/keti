# 8. while, foreach, for문
# C나 PHP 루프문 선언과 비슷하다
# array를 순회할때 for 문보다 foreach문이 편리할 떄가 많다.

my @array = (
    "one",
    "twoo",
    "threee"
);

my $i = 0;

# while 문
while($i < scalar @array) {
    print $i, ": ", $array[$i], " ";
    $i++;
}

print "\n";

# foreach 문
foreach my $i ( 0 .. $#array ) {
    print $i, ": ", $array[$i], " ";
}

print "\n";

for my $i ( 0 .. $#array ) {
    print $i, ": ", $array[$i], " ";
}

print "\n";

# for 문
for(my $i = 0; $i < scalar @array; $i++) {
    print $i, ": ", $array[$i], " ";
}

print "\n";

# until 문
$cnt = 1;
until ($cnt > 10) {
    print "COUNT UP is: $cnt\n";
    $cnt++;
}


$cnt = 10;
do{
    print "COUNTDONW is: $cnt\n";
    $cnt--;
} while ($cnt >0)