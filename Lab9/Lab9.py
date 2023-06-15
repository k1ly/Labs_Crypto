# Кодировочные таблицы base64 и ASCII
# Генерация сверхвозрастающей последовательности
# Старший член последовательности - 100-битное число
# В простейших случаях z = 6 (base64) либо z = 8 (ASCII)
import time


def ReadFile(name_file):
    file_for_only_read = open(name_file, 'r', encoding="utf8")
    return file_for_only_read.read()


def EGCD(a, b):
    if a == 0:
        return b, 0, 1
    else:
        g, y, x = EGCD(b % a, a)
        return g, x - (b // a) * y, y


def GenerateSuperGrowingSequence(len_sequence):
    # 2_535_301_200_456_458_802_993_406_410_752 - 100-битное число
    sequence = [1, 2]
    while len(sequence) != len_sequence:
        next_value = sum(sequence) + 1
        sequence.append(next_value)
    return sequence


def GetPublicKey(sequence, a, n):
    public_key = []
    for elem in sequence:
        public_key.append((elem * a) % n)
    return public_key


def GenerateMinimumValueA(sequence):
    n = sum(sequence) + 1
    counter = 0
    for i in range(2, n):
        if n % i != 0 and counter == 10:
            return i
        elif n % i != 0:
            counter += 1


def EncryptByPackingTheSatchel(public_key, message):
    message_2 = [(len(public_key) - len(bin(ord(i))[2:]))
                 * '0' + bin(ord(i))[2:] for i in message]
    encrypt_message_10 = []
    encrypt_message = []

    for elem in message_2:
        current_encrypt_number = 0
        for i in range(len(elem)):
            if elem[i] == '1':
                current_encrypt_number += public_key[i]
        encrypt_message_10.append(current_encrypt_number)
        encrypt_message.append(chr(current_encrypt_number))
    return encrypt_message_10, ''.join(encrypt_message)


def DecryptByPackingTheSatchel(inverse_a, encrypt_message_10, n, sequence):
    decrypt_message_10 = []
    decrypt_message = []

    for i in encrypt_message_10:
        decrypt_message_10.append((i * inverse_a) % n)

    for i in decrypt_message_10:
        current_symbol = ''
        for index, j in enumerate(sequence[::-1]):
            if j <= i:
                i -= j
                current_symbol += '1'
            else:
                current_symbol += '0'
        decrypt_message.append(chr(int(current_symbol[::-1], 2)))
    return decrypt_message_10, ''.join(decrypt_message)


def main():
    # Эта последовательность используется в дальнейшем для зашифровывания, поэтому len_sequence максимум 13
    len_sequence = 13
    sequence = GenerateSuperGrowingSequence(len_sequence)

    message = ReadFile('text_en.txt')
    message_10 = [ord(i) for i in message]
    message_2 = [[(len_sequence - len(bin(ord(i))[2:])) *
                  '0' + bin(ord(i))[2:] for i in message]]

    encrypt_time = time.time()
    n = sum(sequence) + 1
    a = GenerateMinimumValueA(sequence)

    inverse_a = EGCD(a, n)[1]
    if inverse_a < 0:
        inverse_a += n

    public_key = GetPublicKey(sequence, a, n)
    encrypt_message_10, encrypt_message = EncryptByPackingTheSatchel(
        public_key, message)
    encrypt_time = time.time() - encrypt_time

    decrypt_time = time.time()
    decrypt_message_10, decrypt_message = DecryptByPackingTheSatchel(
        inverse_a, encrypt_message_10, n, sequence)
    decrypt_time = time.time() - decrypt_time

    print(f'----- Задание 1. Генерация сверхвозрастающей последовательности. 100-битное число -----\n'
          f'Последовательность: {len(sequence)}\n {GenerateSuperGrowingSequence(len_sequence)}\n\n'
          f'----- Задание 2. Вычислений нормальной последовательности (открытый ключ) -----\n'
          f'n = {n}\n'
          f'a = {a}\n'
          f'a^(-1) = {inverse_a}\n'
          f'Открытый ключ:\n{public_key}\n\n'

          f'Сообщение (10):\n{message_10}\n'
          f'Сообщение (2):\n{message_2}\n'
          f'Сообщение (латиница):\n{message}\n\n'

          f'----- Задание 3. Зашифровывание сообщения. -----\n'
          f'Зашифрованное сообщение (10):\n{encrypt_message_10}\n'
          f'Зашифрованное сообщение (латиница):\n{encrypt_message}\n\n'

          f'----- Задание 4. Расшифровывание сообщения. -----\n'
          f'Расшифрованное сообщение (10):\n{decrypt_message_10}\n'
          f'Расшифрованное сообщение (латиница):\n{decrypt_message}\n\n'

          f'Сообщение расшифровано {"правильно" if decrypt_message == message else "не правильно"}!\n\n'

          f'----- Задание 5. Оценка времени выполнения операция зашифровывания и расшифровывания -----\n'
          f'Время зашифровывания: {encrypt_time}\n'
          f'Время расшифровывания: {decrypt_time}\n')


main()
