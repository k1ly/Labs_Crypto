import time
import key


def ReadFile(name_file):
    file_for_only_read = open(name_file, 'r', encoding="utf8")
    return file_for_only_read.read()


def GetMessageInTheNumberSystem(message, number_system):
    match number_system:
        case 2:
            message_in_system = ''.join(['0' * (8 - len(bin(ord(i))[2:])) + bin(ord(i))[2:].upper() for i in message])
        case 16:
            message_in_system = ''.join(['0' * (2 - len(hex(ord(i))[2:])) + hex(ord(i))[2:].upper() for i in message])
        case _:
            return message
    return message_in_system


def SplitMesssageIntoBlocks(message_binary):
    blocks_4x16 = []

    for i in range(len(message_binary) // 64):
        blocks_4x16.append(message_binary[i * 64:(i + 1) * 64])
    return blocks_4x16


def PermutationBlock(blocks, number_permutation=0):
    table_permutation = {0: [58, 50, 42, 34, 26, 18, 10, 2,
                             60, 52, 44, 36, 28, 20, 12, 4,
                             62, 54, 46, 38, 30, 22, 14, 6,
                             64, 56, 48, 40, 32, 24, 16, 8,
                             57, 49, 41, 33, 25, 17, 9, 1,
                             59, 51, 43, 35, 27, 19, 11, 3,
                             61, 53, 45, 37, 29, 21, 13, 5,
                             63, 55, 47, 39, 31, 23, 15, 7],
                         1: [40, 8, 48, 16, 56, 24, 64, 32,
                             39, 7, 47, 15, 55, 23, 63, 31,
                             38, 6, 46, 14, 54, 22, 62, 30,
                             37, 5, 45, 13, 53, 21, 61, 29,
                             36, 4, 44, 12, 52, 20, 60, 28,
                             35, 3, 43, 11, 51, 19, 59, 27,
                             34, 2, 42, 10, 50, 18, 58, 26,
                             33, 1, 41, 9, 49, 17, 57, 25]}

    blocks_permutation = []

    for block in blocks:
        current_block = ''
        for j in range(64):
            current_block += block[table_permutation[number_permutation][j] - 1]
        blocks_permutation.append(current_block)
    return blocks_permutation


def SplitBlockIntoBlocksLR(blocks_4x16_permutation):
    blocks_l_r = []
    for block in blocks_4x16_permutation:
        blocks_l_r.append((block[0:32], block[32:]))
    return blocks_l_r


def PBoxExtension(blocks_l_32_r_32, number_extension=0):
    table_extension = {0: [32, 1, 2, 3, 4, 5,
                           4, 5, 6, 7, 8, 9,
                           8, 9, 10, 11, 12, 13,
                           12, 13, 14, 15, 16, 17,
                           16, 17, 18, 19, 20, 21,
                           20, 21, 22, 23, 24, 25,
                           24, 25, 26, 27, 28, 29,
                           28, 29, 30, 31, 32, 1]}

    blocks_l_32_r_48 = []

    for block in blocks_l_32_r_32:
        current_block = ''
        for i in range(48):
            current_block += block[1][table_extension[number_extension][i] - 1]
        blocks_l_32_r_48.append((block[0], current_block))
    return blocks_l_32_r_48


def XORRoundKeys(blocks_l_32_r_48, round_keys_, round_):
    xor_block = ''
    for index, block in enumerate(blocks_l_32_r_48):
        for i in range(len(block[1])):
            if block[1][i] == round_keys_[round_][i]:
                xor_block += '0'
            else:
                xor_block += '1'
        blocks_l_32_r_48[index] = (blocks_l_32_r_48[index][0], xor_block)
        xor_block = ''
    return blocks_l_32_r_48


def XOR(number_list_tuple):
    xor_list_number = []

    for block in number_list_tuple:
        current_xor = ''
        for i in range(len(block[0])):
            if block[0][i] == block[1][i]:
                current_xor += '0'
            else:
                current_xor += '1'
        xor_list_number.append((block[0], current_xor))
    return xor_list_number


def SBoxes(blocks_l_32_r_48_XOR):
    table_s_boxes = {0: [[14, 4, 13, 1, 2, 15, 11, 8, 3, 10, 6, 12, 6, 7, 0, 7],
                         [0, 15, 7, 4, 14, 2, 13, 1, 10, 6, 12, 11, 9, 5, 3, 8],
                         [4, 1, 14, 8, 13, 6, 2, 11, 15, 12, 9, 7, 3, 10, 5, 0],
                         [15, 12, 8, 2, 4, 9, 1, 7, 5, 11, 3, 14, 10, 0, 6, 13]],
                     1: [[15, 1, 8, 14, 6, 11, 3, 4, 9, 7, 2, 13, 12, 0, 5, 10],
                         [3, 13, 4, 7, 15, 2, 8, 14, 12, 0, 1, 10, 6, 9, 11, 5],
                         [0, 14, 7, 11, 10, 4, 13, 1, 5, 8, 12, 6, 9, 3, 2, 15],
                         [13, 8, 10, 1, 3, 15, 4, 2, 11, 6, 7, 12, 0, 5, 14, 9]],
                     2: [[10, 0, 9, 14, 6, 3, 15, 5, 1, 13, 12, 7, 11, 4, 2, 8],
                         [13, 7, 0, 9, 3, 4, 6, 10, 2, 8, 5, 14, 12, 11, 15, 1],
                         [13, 6, 4, 9, 8, 15, 3, 0, 11, 1, 2, 12, 5, 10, 14, 7],
                         [1, 10, 13, 0, 6, 9, 8, 7, 4, 15, 14, 3, 11, 5, 2, 12]],
                     3: [[7, 13, 14, 3, 0, 6, 9, 10, 1, 2, 8, 5, 11, 12, 4, 15],
                         [13, 8, 11, 5, 6, 15, 0, 3, 4, 7, 2, 12, 1, 10, 14, 9],
                         [10, 6, 9, 0, 12, 11, 7, 13, 15, 1, 3, 14, 5, 2, 8, 4],
                         [3, 15, 0, 6, 10, 1, 13, 8, 9, 4, 5, 11, 12, 7, 2, 14]],
                     4: [[2, 12, 4, 1, 7, 10, 11, 6, 8, 5, 3, 14, 13, 0, 14, 9],
                         [14, 11, 2, 12, 4, 7, 13, 1, 5, 0, 15, 10, 3, 9, 8, 6],
                         [4, 2, 1, 11, 10, 13, 7, 8, 15, 9, 12, 5, 6, 3, 0, 14],
                         [11, 8, 12, 7, 1, 14, 2, 13, 6, 15, 0, 9, 10, 4, 5, 3]],
                     5: [[12, 1, 10, 15, 9, 2, 6, 8, 0, 13, 3, 4, 14, 7, 5, 11],
                         [10, 15, 4, 2, 7, 12, 9, 5, 6, 1, 13, 14, 0, 11, 3, 8],
                         [9, 14, 15, 5, 2, 8, 12, 3, 7, 0, 4, 10, 1, 13, 11, 6],
                         [4, 3, 2, 12, 9, 5, 15, 10, 11, 14, 1, 7, 6, 0, 8, 13]],
                     6: [[4, 11, 2, 14, 15, 0, 8, 13, 3, 12, 9, 7, 5, 10, 6, 1],
                         [13, 0, 11, 7, 4, 9, 1, 10, 14, 3, 5, 12, 2, 15, 8, 6],
                         [1, 4, 11, 13, 12, 3, 7, 13, 10, 15, 6, 8, 0, 5, 9, 2],
                         [6, 11, 13, 8, 1, 4, 10, 7, 9, 5, 0, 15, 14, 2, 3, 12]],
                     7: [[13, 2, 8, 4, 6, 15, 11, 1, 10, 9, 3, 14, 5, 0, 12, 7],
                         [1, 15, 13, 8, 10, 3, 7, 4, 12, 5, 6, 11, 0, 14, 9, 2],
                         [7, 11, 4, 1, 9, 12, 14, 2, 0, 6, 10, 13, 15, 3, 5, 8],
                         [2, 1, 14, 7, 4, 10, 8, 13, 15, 12, 9, 0, 3, 5, 6, 11]]}

    blocks_split = []
    for index_, block in enumerate(blocks_l_32_r_48_XOR):
        for i in range(8):
            blocks_split.append(block[1][i * 6:(i+1) * 6])
        block_after_permutation = ''
        for index, block_after_split in enumerate(blocks_split):
            row = int(block_after_split[0] + block_after_split[5], 2)
            col = int(block_after_split[1:5], 2)
            current_block = (4 - len(bin(table_s_boxes[index][row][col])[2:])) * '0' + \
                            bin(table_s_boxes[index][row][col])[2:]
            block_after_permutation += current_block
        blocks_l_32_r_48_XOR[index_] = (blocks_l_32_r_48_XOR[index_][0], block_after_permutation)
        blocks_split = []
    return blocks_l_32_r_48_XOR


def PBoxDirect(blocks_l_32_r_48_XOR_S, number_permutation=0):
    table_permutation = {0: [16, 7, 20, 21, 29, 12, 28, 17,
                             1, 15, 23, 26, 5, 18, 31, 19,
                             2, 8, 24, 14, 32, 27, 3, 9,
                             19, 13, 30, 6, 22, 11, 4, 25]}
    for index, block in enumerate(blocks_l_32_r_48_XOR_S):
        block_after_permutation = ''
        for i in range(len(block[1])):
            block_after_permutation += block[1][table_permutation[number_permutation][i] - 1]
        blocks_l_32_r_48_XOR_S[index] = (blocks_l_32_r_48_XOR_S[index][0], block_after_permutation)
    return blocks_l_32_r_48_XOR_S


def EncryptAndDecrypt(message_2, round_keys_):
    # print(message_2)
    blocks_4x16 = SplitMesssageIntoBlocks(message_2)
    # print(blocks_4x16)
    blocks_4x16_permutation = PermutationBlock(blocks_4x16, number_permutation=0)
    # print(blocks_4x16_permutation)
    blocks_l_32_r_32 = SplitBlockIntoBlocksLR(blocks_4x16_permutation)
    # print(blocks_l_32_r_32)
    # Прохождение 16 раундов
    for i in range(16):
        blocks_r_32 = [block_[1] for block_ in blocks_l_32_r_32]
        # print(blocks_r_32)
        blocks_l_32_r_48_P = PBoxExtension(blocks_l_32_r_32)
        # print(blocks_l_32_r_48_P)
        blocks_l_32_r_48_P_XOR = XORRoundKeys(blocks_l_32_r_48_P, round_keys_, i)  # Работает правильно
        # print(blocks_l_32_r_48_P_XOR)
        blocks_l_32_r_48_P_XOR_S = SBoxes(blocks_l_32_r_48_P_XOR)  # Работает правильно
        # print(blocks_l_32_r_48_P_XOR_S)
        blocks_l_32_r_48_P_XOR_S_P = PBoxDirect(blocks_l_32_r_48_P_XOR_S)  # Работает правильно
        # print(blocks_l_32_r_48_P_XOR_S_P)
        blocks_l_32_r_48_P_XOR_S_P = XOR(blocks_l_32_r_48_P_XOR_S_P)
        # print(blocks_l_32_r_48_P_XOR_S_P)
        for index, block in enumerate(blocks_l_32_r_48_P_XOR_S_P):  # Работает правильно
            blocks_l_32_r_32[index] = (blocks_r_32[index], block[1])
            # print(blocks_l_32_r_32)
            # print()

    blocks_l_32_r_32 = PermutationBlock([block[1] + block[0] for block in blocks_l_32_r_32], number_permutation=1)
    # print(blocks_l_32_r_32)
    encrypt_message = ''.join([block for block in blocks_l_32_r_32])
    return encrypt_message


def main():
    key_message = 'maksimda'
    message = ReadFile('en_text.txt')

    message_2 = GetMessageInTheNumberSystem(message, 2)
    message_16 = GetMessageInTheNumberSystem(message, 16)
    round_keys_ = key.PrepareRoundKeys(key_message=key_message)

    message_2 += (64 - (len(message_2) % 64)) * '0'

    encrypt_time = time.time()
    encrypt_message_2 = EncryptAndDecrypt(message_2, round_keys_)
    encrypt_time = time.time() - encrypt_time

    encrypt_message = ''.join([chr(int(encrypt_message_2[i * 8: (i + 1) * 8], 2))
                               for i in range(len(encrypt_message_2) // 8)
                               if 0 < int(encrypt_message_2[i * 8: (i + 1) * 8], 2) <= 255])
    encrypt_message_16 = ''.join([hex(int(encrypt_message_2[i * 8: (i + 1) * 8], 2))[2:].upper()
                                 for i in range(len(encrypt_message_2) // 8)
                                 if 0 < int(encrypt_message_2[i * 8: (i + 1) * 8], 2) <= 255])
    # print('--- --- ---')
    decrypt_time = time.time()
    decrypt_message_2 = EncryptAndDecrypt(encrypt_message_2, round_keys_[::-1])
    decrypt_time = time.time() - decrypt_time

    decrypt_message = ''.join([chr(int(decrypt_message_2[i * 8: (i + 1) * 8], 2))
                               for i in range(len(decrypt_message_2) // 8)
                               if 0 < int(decrypt_message_2[i * 8: (i + 1) * 8], 2) <= 255])
    decrypt_message_16 = ''.join([hex(int(decrypt_message_2[i * 8: (i + 1) * 8], 2))[2:].upper()
                                 for i in range(len(decrypt_message_2) // 8)
                                 if 0 < int(decrypt_message_2[i * 8: (i + 1) * 8], 2) <= 255])

    print(f'Прямой порядок раундовых ключей:\n{round_keys_}\n'
          f'Обратный порядок раундовых ключей:\n{round_keys_[::-1]}\n'
          f'\nСообщение (латиница): {message}\n'
          f'Сообщение (2): {message_2}\n'
          f'Сообщение (16): {message_16}\n'
          f'Длина сообщения (латиница, 2, 16): {len(message), len(message_2), len(message_16)}\n'
          
          f'\nЗашифрованное сообщение(латиница): {encrypt_message}\n'
          f'Зашифрованное сообщение(2): {encrypt_message_2}\n'
          f'Зашифрованное сообщение(16): {encrypt_message_16}\n'
          f'Длина зашифрованного сообщения (латиница, 2, 16): '
          f'{len(encrypt_message), len(encrypt_message_2), len(encrypt_message_16)}\n'
          f'Время зашифровывания: {encrypt_time}\n'
          
          f'\nРасшифрованное сообщение(латиница): {decrypt_message}\n'
          f'Расшифрованное сообщение(2): {decrypt_message_2}\n'
          f'Расшифрованное сообщение(16): {decrypt_message_16}\n'
          f'Длина расшифрованного сообщения (латиница, 2, 16): '
          f'{len(decrypt_message), len(decrypt_message_2), len(decrypt_message_16)}\n'
          f'Время расшифровывания: {decrypt_time}\n')

    print(f'Количество несовпадающих битов исходного и расшифрованного сообщения (2): '
          f'{[message_2[i] == decrypt_message_2[i] for i in range(len(message_2))].count(False)}\n')


main()
