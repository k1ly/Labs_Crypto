from random import randint
import time
from BBS import BBS
import prime
import sys


class BBS_Generator:
    def __init__(self, max, n):
        self.max = max
        self.n = n
        self.numbers_gen = []

    def __is_good_prime(self, number):
        return number % 4 == 3 and prime.miller_rabin(number)

    def __choose_prime_number(self):
        random = randint(3, self.max - 1)
        while not self.__is_good_prime(random):
            random = randint(3, self.max - 1)
        return random

    def generate_numbers(self, nb_to_generate):
        print("** Choose p prime number **")
        p = self.__choose_prime_number()
        print("==> p = ", p)
        print("** Choose q prime number **")
        q = self.__choose_prime_number()
        print("==> q = ", q)
        seed = randint(1, self.max - 1)
        bbs = BBS(p, q, seed)

        for _ in range(nb_to_generate):
            self.numbers_gen.append(bbs.get_random_int(self.n))
        print("** End generation BBS **")
        del p, q, seed, bbs

    def print(self):
        i = 0
        for x in self.numbers_gen:
            print("number ", i, " random value = ", x)
            i += 1


def main():
    # Command line argument
    # [1] ==> max number where the prime numbers are chosen
    # [2] ==> length in bits for the generated number
    # [3] ==> number of random number to generate
    max_prime_number_arg = int(sys.argv[1])
    nb_bits_output = int(sys.argv[2])
    nb_numbers_to_generate = int(sys.argv[3])

    bbs = BBS_Generator(max_prime_number_arg, nb_bits_output)
    generation_time = time.time()
    bbs.generate_numbers(nb_numbers_to_generate)
    generation_time = time.time() - generation_time
    print(f"Generation time: {generation_time}")
    bbs.print()


if __name__ == "__main__":
    main()
