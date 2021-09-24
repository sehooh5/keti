import random

num = str(random.randint(0000, 2767))
if len(num) == 3:
    print("nope", f"0{num}")
elif len(num) == 2:
    print("nope", f"00{num}")
elif len(num) == 1:
    print("nope", f"00{num}")
else:
    print("okay", num)
