def MakeBinaryKey(key_message):
    key_64 = ''.join([(8 - len(bin(ord(i))[2:])) * '0' + bin(ord(i))[2:] for i in key_message])
    if len(key_64) != 64:
        key_64 = key_64[0:64]
        key_64 += '0' * (64 - len(key_64))
    return key_64


def RearrangeKeyBits(key_64, number_permutation=0):
    table_permutation = {0: [57, 49, 41, 33, 25, 17, 9, 1, 58, 50, 42, 34, 26, 18,
                             10, 2, 59, 51, 43, 35, 27, 19, 11, 3, 60, 52, 44, 36,
                             63, 55, 47, 39, 31, 23, 15, 7, 62, 54, 46, 38, 30, 22,
                             14, 6, 61, 53, 45, 37, 29, 21, 13, 5, 28, 20, 12, 4]}
    key_rearranged_56 = []
    for i in range(len(table_permutation[number_permutation])):
        key_rearranged_56.append(key_64[table_permutation[number_permutation][i] - 1])
    return ''.join(key_rearranged_56)


def SplitBlockIntoTwoBlocks(key_56):
    key_c = key_56[0:28]
    key_d = key_56[28:]
    return key_c, key_d


def GetRoundKeys(key_c, key_d):
    shifts = [1, 1, 2, 2, 2, 2, 2, 2, 1, 2, 2, 2, 2, 2, 2, 1]

    current_key_c = key_c[:]
    current_key_d = key_d[:]
    round_keys = []

    for i in range(len(shifts)):
        current_key_c = current_key_c[shifts[i]:] + current_key_c[0:shifts[i]]
        current_key_d = current_key_d[shifts[i]:] + current_key_d[0:shifts[i]]
        round_keys.append((current_key_c, current_key_d))
    return round_keys


def RearrangingCompression(keys_round_c_d, number_permutation=0):
    table_permutation = {0: [14, 17, 11, 24, 1, 5, 3, 28,
                             15, 6, 21, 10, 23, 19, 12, 4,
                             26, 8, 16, 7, 27, 20, 13, 2,
                             41, 52, 31, 37, 47, 55, 30, 40,
                             51, 45, 33, 48, 44, 49, 39, 56,
                             34, 53, 46, 42, 50, 36, 29, 32]}

    keys_round_ = []

    for i in range(len(keys_round_c_d)):
        current_keys_c_d = keys_round_c_d[i][0] + keys_round_c_d[i][1]
        key_48 = ''
        for j in range(48):
            key_48 += current_keys_c_d[table_permutation[number_permutation][j] - 1]
        keys_round_.append(key_48)
    return keys_round_


def PrepareRoundKeys(key_message):
    key_64 = MakeBinaryKey(key_message)
    key_56 = RearrangeKeyBits(key_64=key_64)
    key_c, key_d = SplitBlockIntoTwoBlocks(key_56)
    keys_round_c_d = GetRoundKeys(key_c, key_d)
    keys_round_ = RearrangingCompression(keys_round_c_d)

    print(f'Ключевое слово: {key_message}\n'
          f'64 битовый ключ: {key_64}\n'
          f'56-битовый ключ: {key_56}\n'
          f'Левый 28-битный блок C0: {key_c}\n'
          f'Правый 28-битный блок D0: {key_d}\n'
          f'Список раундовых 28-битных C0 и D0 ключей: {keys_round_c_d}\n'
          f'Список раундовых 48-битовых ключей: {keys_round_}\n')

    return keys_round_
