import time
import matplotlib.pyplot as plt
import numpy as np
import math
import random


def ReadFile(name_file):
    file_for_only_read = open(name_file, 'r', encoding="utf8")
    return file_for_only_read.read()


def BuildHistogram(list_time, list_value_parameter):
    fig, ax = plt.subplots(1, 1)
    ax[0].bar(list_time, list_value_parameter)
    plt.show()


def SearchForPrimeNumbersOnTheIntervalUsingRecursion(listNumber=None):
    if listNumber is None:
        listNumber = []

    if len(listNumber) == 2:
        listPrimeNumber = []
        traversableArray = np.arange(listNumber[0], listNumber[1] + 1, 1)

        if listNumber != [2, 3]:
            primeNumbersUpToUpperBound = \
                SearchForPrimeNumbersOnTheIntervalUsingRecursion(
                    [2, math.ceil(math.pow(listNumber[1], 0.5))])[0]
        else:
            primeNumbersUpToUpperBound = [2, 3]

        for i in range(len(traversableArray)):
            for j in range(len(primeNumbersUpToUpperBound)):
                if (traversableArray[i] % primeNumbersUpToUpperBound[j] == 0 and traversableArray[i] !=
                        primeNumbersUpToUpperBound[j]):
                    break
            else:
                listPrimeNumber.append(traversableArray[i])

    return listPrimeNumber, len(listPrimeNumber)


def InverseNumber(a, N):
    if N == 0:
        return a, 1, 0
    else:
        d, x, y = InverseNumber(N, a % N)
        return d, y, x - y * (a // N)


def IsPrimitiveRoot(number, p):
    remains = set([(number ** i) % p for i in range(1, p)])
    return len(remains) == p - 1


def IsPrimitiveRoot(number, p):
    remains = set([(number ** i) % p for i in range(1, p)])
    return len(remains) == p - 1


def GenerateMainComponents(p):
    for i in range(2, p):
        if IsPrimitiveRoot(i, p):
            g = i
            break

    x = int(random.random() * (p - 1))
    y = (g ** x) % p

    public_key = p, g, y
    private_key = p, g, x
    k = int(random.random() * (p - 1))
    return public_key, private_key, k


def EncryptEG(message, public_key, k):
    p, g, y = public_key
    M = [ord(i) for i in message]

    encrypt_message = []
    for i in M:
        encrypt_message.append(((g ** k) % p, (y ** k * i) % p))
    return encrypt_message


def DecryptEG(encrypt_message, private_key, k):
    p, g, x = private_key

    decrypt_message = []
    for a_b in encrypt_message:
        decrypt_message.append(chr((a_b[1] * (a_b[0] ** (p - x - 1))) % p))
    return ''.join(decrypt_message)


def ElGamal(message, p=None):
    if p is None or p > 200:
        p = 191

    message_10 = [ord(i) for i in message]

    public_key, private_key, k = GenerateMainComponents(p)

    encrypt_time = time.time()
    encrypt_message = EncryptEG(message, public_key, k)
    encrypt_time = time.time() - encrypt_time

    decrypt_time = time.time()
    decrypt_message = DecryptEG(encrypt_message, private_key, k)
    decrypt_time = time.time() - decrypt_time

    print(f'----- Входная информация -----\n'
          f'Сообщение: {message}\n'
          f'Сообщение(10): {message_10}\n'
          f'p = {p}\n'
          f'----- Ключи -----\n'
          f'Открытый ключ: {public_key}\n'
          f'Закрытый ключ: {private_key}\n'
          f'----- Зашифровывание -----\n'
          f'Открытый ключ: {public_key}\n'
          f'k = {k}\n'
          f'Зашифрованное сообщение: {encrypt_message}\n'
          f'----- Расшифровывание -----\n'
          f'Закрытый ключ: {private_key}\n'
          f'Расшифрованное сообщение: {decrypt_message}\n'
          f'----- Успешность расшифровывания -----\n'
          f'Сообщение расшифровано {"правильно" if message == decrypt_message else "неправильно"}\n'
          f'Время шифрования: {encrypt_time}\n'
          f'Время расшифрования: {decrypt_time}\n')


def RSA(message):
    # p = max(SearchForPrimeNumbersOnTheIntervalUsingRecursion([2, 25])[0])
    # q = max(SearchForPrimeNumbersOnTheIntervalUsingRecursion([2, 6])[0])

    p = 101
    q = 439

    n = p * q
    e = 17
    function_euler_n = (p - 1) * (q - 1)

    e_inverse = InverseNumber(e, function_euler_n)[1]
    d = e_inverse % function_euler_n

    public_key = e, n
    secret_key = d, n

    message_10 = [ord(i) for i in message]
    encrypt_message = []
    decrypt_message = []

    encrypt_time = time.time()

    for i in message_10:
        encrypt_message.append((i ** e) % n)

    encrypt_time = time.time() - encrypt_time

    decrypt_time = time.time()

    for i in encrypt_message:
        decrypt_message.append((i ** d) % n)

    decrypt_time = time.time() - decrypt_time

    print(f'----- Основные компоненты -----\n'
          f'Число p: {p}\n'
          f'Число q: {q}\n'
          f'Число n: {n}\n'
          f'Число e: {e}\n'
          f'Число e^(-1): {e_inverse}\n'
          f'Число d: {d}\n'
          f'Функция Эйлера для n: {function_euler_n}\n'
          f'----- Ключи -----\n'
          f'Публичный ключ: {public_key}\n'
          f'Тайный ключ: {secret_key}\n'
          f'----- Зашифровывание -----\n'
          f'Сообщение: {message_10}\n'
          f'Зашифрованное сообщение: {encrypt_message}\n'
          f'----- Расшифровывание -----\n'
          f'Расшифрованное сообщение: {decrypt_message}\n'
          f'----- Успешность расшифровывания -----\n'
          f'Сообщение расшифровано {"правильно" if decrypt_message == message_10 else "неправильно"}\n'
          f'Время шифрования: {encrypt_time}\n'
          f'Время расшифрования: {decrypt_time}\n')


def main():
    print(f'----- Задание 2-1. Зашифровать и расшифровать текстовые документы на основе RSA -----')
    message = 'Dashchinskii Maksim Leonidovich'
    RSA(message)

    print(f'----- Задание 2-2. Зашифровать и расшифровать текстовые документы на основе Эль-Гамаля ----- ')
    message = 'Dashchinskii Maksim Leonidovich'
    p = 191
    ElGamal(message, p)


main()
