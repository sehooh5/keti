# 9. array 함수
# array 자료형 뿐만 아니라 함수또한 지원

my @array = (
    "one", "twoo", "threee", "fourrrr"
);

print join(", ", @array), "\r\n";
print "NORMAL : ", @array, "\r\n";
print "REVERSE : ", reverse(@array), "\r\n";
print join(", ", reverse(@array)), "\r\n";
pop(@array);
print "pop : ", join(", ", @array), "\r\n";
push(@array, "fiveeeee");
print "push : " , join(", ", @array), "\r\n";
shift(@array);
print "shift : ", join(", ", @array), "\r\n";
#splice
print "splice : ", join(", ", @array), "\r\n";
#unshift
print "unshift : ", join(", ", @array), "\r\n";
