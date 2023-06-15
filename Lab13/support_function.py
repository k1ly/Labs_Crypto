def InverseNumber(a: int, N: int) -> int:
    if N == 0:
        return a, 1, 0
    else:
        d, x, y = InverseNumber(N, a % N)
        return d, y, x - y * (a // N)