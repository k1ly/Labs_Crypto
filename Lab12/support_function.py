import math


def InverseNumber(a: int, N: int) -> int:
    if N == 0:
        return a, 1, 0
    else:
        d, x, y = InverseNumber(N, a % N)
        return d, y, x - y * (a // N)


def GetFirstMutuallyPrimeNumber(number: int) -> int:
    def gcd(a, b):
        while b != 0:
            a, b = b, a % b
        return a

    for i in range(2, int(number ** 0.5) + 1):
        if gcd(number, i) == 1:
            return i

    return None


def IsPrimitiveRoot(number: int, p: int) -> bool:
    remains = [False] * (p - 1)

    for i in range(1, p):
        power = FastPower(number, i, p)
        if remains[power - 1]:
            return False
        remains[power - 1] = True

    return True


def GeneratePrimitiveRoot(p: int) -> int:
    def is_prime(n: int) -> bool:
        if n <= 1:
            return False
        if n <= 3:
            return True
        if n % 2 == 0 or n % 3 == 0:
            return False
        i = 5
        while i * i <= n:
            if n % i == 0 or n % (i + 2) == 0:
                return False
            i += 6
        return True

    def euler_totient(n: int) -> int:
        result = n
        i = 2
        while i * i <= n:
            if n % i == 0:
                while n % i == 0:
                    n //= i
                result -= result // i
            i += 1
        if n > 1:
            result -= result // n
        return result

    if not is_prime(p):
        return None

    for g in range(2, p):
        if FastPower(g, euler_totient(p), p) == 1:
            return g

    return None


def GetBByKAndP(k: int, p: int, x: int, a: int, hash_message: int) -> int:
    m = p - 1
    gcd, c, d = InverseNumber(k, m)
    if gcd == 1:
        inverse_a = c % m
        return (((hash_message - x * a) % m) * inverse_a) % m


def GetDivisors(number: int) -> int:
    for i in range(2, number):
        if number % i == 0:
            return i


def FindOrder(q: int, mod: int) -> int:
    result = 2
    power = 0

    while power != 1:
        power = pow(result, q, mod)  # Используем встроенную функцию pow
        if power == 1:
            break
        result += 1
    return result - 1


def GetYByGAndP(g: int, p: int, x: int) -> int:
    gcd, c, d = InverseNumber(g, p)
    c = (c % p + p) % p
    return pow(c, x, p)


def FastPower(base: int, exponent: int, modulus: int) -> int:
    result = 1
    while exponent > 0:
        if exponent % 2 == 1:
            result = (result * base) % modulus
        base = (base * base) % modulus
        exponent //= 2
    return result
