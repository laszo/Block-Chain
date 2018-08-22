p = 17
q = 19
N = p * q
L = 0
for L in range(2, N + 1):
    if L % (p - 1) == 0 and L % (q - 1) == 0:
        break
print(L)
E = 0


# E L 的最大公约数为1

def gcd(a, b):
    m = 1
    for i in range(1, a + 1):
        if a % i == 0 and b % i == 0:
            if i > m:
                m = i
    return m


for E in range(2, L + 1):
    g = gcd(E, L)
    if g == 1:
        break

print(E)

for D in range(2, L + 1):
    if E * D % L == 1:
        break

print(D)
print(E, N)
print(D, N)
