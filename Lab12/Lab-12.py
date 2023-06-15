import random
import time

from support_function import *


def EDSBasedOnRsa(message: str, p: int, q: int):
    # Подготовка
    verification_time = time.process_time()
    n = p * q
    euler_function = (p - 1) * (q - 1)
    e = GetFirstMutuallyPrimeNumber(euler_function)
    d = InverseNumber(e, euler_function)[1] % euler_function
    print('--- Подготовка ---\n'
          f'p = {p}\n'
          f'q = {q}\n'
          f'n = {n}\n'
          f'euler_function = {euler_function}\n'
          f'e = {e}\n'
          f'd = {d}')

    # Отправитель
    hash_message_sender = hash(message) % n
    encrypt_hash = FastPower(hash_message_sender, e, n)
    print(f'--- Отправитель ---\n'
          f'H(message) = {hash_message_sender}\n'
          f'S(H(message)) = {encrypt_hash}\n'
          f'Отправлено {encrypt_hash} и идентификатор отправителя')

    # Получатель
    hash_message_recipient = hash(message) % n
    decrypt_hash = FastPower(encrypt_hash, d, n)
    comparison_result = decrypt_hash == hash_message_recipient
    print(f'--- Получатель ---\n'
          f'H(message) = {hash_message_recipient}\n'
          f'D(S(H(message)))) = {decrypt_hash}\n'
          f'Подпись {"верифицирована!" if comparison_result else "не верифицирована!"}')

    verification_time = time.process_time() - verification_time
    print(f'--- Анализ ---\n'
          f'Время верификации: {verification_time}')


def EDSBasedElGamal(message: str, p: int):
    # Подготовка
    verification_time = time.process_time()
    g = GeneratePrimitiveRoot(p)
    x = int(random.random() * p)
    y = FastPower(g, x, p)
    print(f'--- Подготовка ---\n'
          f'p = {p}\n'
          f'g = {g}\n'
          f'x = {x}\n'
          f'y = {y}')

    # Отправитель
    k = GetFirstMutuallyPrimeNumber(p - 1)
    hash_message_sender = hash(message) % p
    a = FastPower(g, k, p)
    b = GetBByKAndP(k, p, x, a, hash_message_sender)
    print(f'--- Отправитель ---\n'
          f'k = {k}\n'
          f'a = {a}\n'
          f'b = {b}\n'
          f'H(message) = {hash_message_sender}\n'
          f'Отправлено S{a, b} и {message}')

    # Получатель
    hash_message_recipient = hash(message) % p
    comparison_result = (FastPower(y, a, p) * FastPower(a, b, p)
                         ) % p == FastPower(g, hash_message_recipient, p)
    print(f'--- Получатель ---\n'
          f'H(message) = {hash_message_recipient}\n'
          f'Подпись {"верифицирована!" if comparison_result else "не верифицирована!"}')

    verification_time = time.process_time() - verification_time
    print(f'--- Анализ ---\n'
          f'Время верификации: {verification_time}')


def EDSBasedSchnorr(message: str, p: int):
    # Подготовка
    verification_time = time.process_time()
    q = GetDivisors(p - 1)
    x = int(random.random() * q)
    g = FindOrder(q, p)
    y = GetYByGAndP(g, p, x)
    print(f'--- Подготовка ---\n'
          f'p = {p}\n'
          f'q = {q}\n'
          f'g = {g}\n'
          f'x = {x}\n'
          f'y = {y}')

    # Отправитель
    k = int(random.random() * q)
    a = pow(g, k, p)
    hash_message_sender = hash(message + str(a)) % p
    b = pow(k + x * hash_message_sender, 1, q)
    print(f'--- Отправитель ---\n'
          f'k = {k}\n'
          f'a = {a}\n'
          f'H(message||a) = {hash_message_sender}\n'
          f'b = {b}\n'
          f'Отправлено {message}||S{hash_message_sender, b}')

    # Получатель
    X = pow(FastPower(g, b, p) * FastPower(y, hash_message_sender, p), 1, p)
    hash_message_recipient = hash(message + str(X)) % p
    comparison_result = hash_message_recipient == hash_message_sender
    print(f'--- Получатель ---\n'
          f'X = {X}\n'
          f'H(message||X) = {hash_message_recipient}\n'
          f'Подпись {"верифицирована!" if comparison_result else "не верифицирована!"}')

    verification_time = time.process_time() - verification_time
    print(f'--- Анализ ---\n'
          f'Время верификации: {verification_time}')


def main():
    message = 'Maksim'
    p = 816463523604803778126518873537
    q = 509890776950785452921107158471

    print(f'----- ЭЦП на основе алгоритма RSA -----')
    EDSBasedOnRsa(message, p, q)
    print()

    p = 3856881264167
    print(f'----- ЭЦП на основе алгоритма Эль-Гамаля -----')
    EDSBasedElGamal(message, p)
    print()

    p = 3286177
    print(f'----- ЭЦП на основе алгоритма Шнорра -----')
    EDSBasedSchnorr(message, p)
    print()


if __name__ == '__main__':
    main()
