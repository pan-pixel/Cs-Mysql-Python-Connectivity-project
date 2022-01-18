import string
import random
digs = string.digits
chars=string.ascii_uppercase
b = ''
a = random.choice(chars)
for i in range(9):
    b += random.choice(digs)
c = a+b
print(c)
