from support_function import read_file, build_histogram
import time


def expansion_to_multiplicity_of_512(message_binary):
    if len(message_binary) % 512 < 448 and len(message_binary) % 512 != 0:
        extended_block = '1' + (448 - len(message_binary) % 512 - 1) * '0' \
                         + (64 - len(bin(len(message_binary))
                            [2:])) * '0' + bin(len(message_binary))[2:]
    elif 448 < len(message_binary) % 512 < 512:
        extended_block = '1' + (512 - 1 - len(message_binary) % 512) * '0' \
                         + 448 * '0' + \
            (64 - len(bin(len(message_binary))[2:])
             ) * '0' + bin(len(message_binary))[2:]
    else:
        extended_block = '1' + 447 * '0' + \
            (64 - len(bin(len(message_binary))[2:])
             ) * '0' + bin(len(message_binary))[2:]
    extended_message = message_binary + extended_block
    return extended_message


def split_into_blocks(block, size_blocks):
    return [block[i * size_blocks: (i + 1) * size_blocks] for i in range(len(block) // size_blocks)]


def expansion_to_80_blocks(blocks_16_32):
    blocks_80_32 = [int(i, 2) for i in blocks_16_32]

    for i in range(16, 80):
        blocks_80_32.append(
            (blocks_80_32[i - 3] ^ blocks_80_32[i - 8] ^ blocks_80_32[i - 14] ^ blocks_80_32[i - 16]) << 1)
    return blocks_80_32


def sha_1(message: str, output_in_console: bool):
    message_binary = ''.join(
        [(16 - len(bin(ord(i))[2:])) * '0' + bin(ord(i))[2:] for i in message])
    extended_message = expansion_to_multiplicity_of_512(message_binary)
    blocks_512 = split_into_blocks(extended_message, 512)

    A = 0x67452301
    B = 0xEFCDAB89
    C = 0x98BADCFE
    D = 0x10325476
    E = 0xC3D2E1F0

    for block in blocks_512:
        blocks_16_32 = split_into_blocks(block, 32)

        blocks_80_32 = expansion_to_80_blocks(blocks_16_32)
        a, b, c, d, e = A, B, C, D, E

        for i in range(80):
            if 0 <= i <= 19:
                f = (b & c) | (~b & d)
                k = 0x5A827999
            elif 20 <= i <= 39:
                f = b ^ c ^ d
                k = 0x6ED9EBA1
            elif 40 <= i <= 59:
                f = (b & c) | (b & d) | (c & d)
                k = 0x8F1BBCDC
            else:
                f = b ^ c ^ d
                k = 0xCA62C1D6
            temp = ((a << 5) + f + e + k + blocks_80_32[i]) % (2 ** 32)
            e = d
            d = c
            c = b << 30
            b = a
            a = temp
        A += a
        B += b
        C += c
        D += d
        E += e

    A_32 = (32 - len(bin((A + a) % (2 ** 32))
            [2:])) * '0' + bin((A + a) % (2 ** 32))[2:]
    B_32 = (32 - len(bin((B + b) % (2 ** 32))
            [2:])) * '0' + bin((B + b) % (2 ** 32))[2:]
    C_32 = (32 - len(bin((C + c) % (2 ** 32))
            [2:])) * '0' + bin((C + c) % (2 ** 32))[2:]
    D_32 = (32 - len(bin((D + d) % (2 ** 32))
            [2:])) * '0' + bin((D + d) % (2 ** 32))[2:]
    E_32 = (32 - len(bin((E + e) % (2 ** 32))
            [2:])) * '0' + bin((E + e) % (2 ** 32))[2:]

    digest_2 = A_32 + B_32 + C_32 + D_32 + E_32
    digest_16 = ''.join([hex(int(digest_2[i * 4: (i + 1) * 4], 2))[2:]
                        for i in range(len(digest_2) // 4)]).upper()
    if output_in_console:
        print(f'Исходное сообщение и его длина: {len(message_binary)} {message_binary}\n'
              f'Расширенное сообщение и его длина: {len(extended_message)} {extended_message}\n'
              f'Сообщение, разбитое на 512 битные блоки: {blocks_512}\n'
              f'Полученный хэш (дайджест) в двоичной системе: {digest_2}\n'
              f'Длина хэша (дайджест) в двоичной системе: {len(digest_2)}\n'
              f'Полученный хэш (дайджест) в шестнадцатеричной системе: {digest_16}\n'
              f'Длина хэша (дайджест) в шестнадцатеричной системе: {len(digest_16)}\n'
              )


def main():
    print(f'----- Задание 1 -----')
    message = read_file('text_en.txt', 100)
    sha_1(message, True)

    print(f'----- Задание 2 -----')
    message_length, calculation_time = [], []
    for i in range(10):
        hashing_time = time.time()
        message = read_file('text_en.txt', int(100 + i * 10))
        sha_1(message, False)
        hashing_time = time.time() - hashing_time

        message_length.append(len(message))
        calculation_time.append(hashing_time)

    build_histogram(message_length, calculation_time)
    print(f'Значение длины сообщения: {message_length}\n'
          f'Значение времени вычисления: {calculation_time}\n')


main()
