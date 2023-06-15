class BBS:
    """
    p is prime number
    q is a prime number
    seed is the x0
    mfactor is compute by p * q
    """

    def __init__(self, p, q, seed):
        self.p = p
        self.q = q
        self.seed = seed
        self.xn = seed
        self.m_factor = p * q

    """
    generation of bits string, n is the lenght of the number to generate in bits
    """

    def get_random(self, n):
        out = ''
        for i in range(n):
            self.xn = pow(self.xn, 2, self.m_factor)
            out += str(self.xn % 2)
        return out

    """
    The same as above but return the value as an integer
    """

    def get_random_int(self, n):
        return int(self.get_random(n), 2)