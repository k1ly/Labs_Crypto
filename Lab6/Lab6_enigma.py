import string


def get_rotors(list_rotors):
    dict_rotors = {'I': 'EKMFLGDQVZNTOWYHXUSPAIBRCJ',
                   'II': 'AJDKSIRUXBLHWTMCQGZNPYFVOE',
                   'III': 'BDFHJLCPRTXVZNYEIWGAKMUSQO',
                   'IV': 'ESOVPZJAYQUIRHXLNFTGKDCMWB',
                   'V': 'VZBRGITYUPSDNHLXAWMJQOFECK',
                   'VI': 'JPGVOUMFYQBENHZRDKASXLICTW',
                   'VII': 'NZJHGRCXMYSWBOUFAIVLPEKQDT',
                   'VIII': 'FKQHTLXOCBJSPDZRAMEWNIUYGV',
                   'Beta': 'LEYJVCNIXWPBQMDRTAKZGFUHOS',
                   'Gamma': 'FSOKANUERHMBTIYCWLQPZXVGJD'}

    return {f'{key}': dict_rotors[key] for key in dict_rotors.keys() if key in list_rotors}


def get_reflector(reflector):
    dict_reflectors = {'B': ['AY', 'BR', 'CU', 'DH', 'EQ', 'FS', 'GL', 'IP', 'JX', 'KN', 'MO', 'TZ', 'VW'],
                       'C': ['AF', 'BV', 'CP', 'DJ', 'EI', 'GO', 'HY', 'KR', 'LZ', 'MX', 'NW', 'TQ', 'SU'],
                       'B Dunn': ['AE', 'BN', 'CK', 'DQ', 'FU', 'GY', 'HW', 'IJ', 'LO', 'MP', 'RX', 'SZ', 'TV'],
                       'C Dunn': ['AR', 'BD', 'CO', 'EJ', 'FN', 'GT', 'HK', 'IV', 'LM', 'PW', 'QZ', 'SX', 'UY']}
    return {f'{key}': dict_reflectors[key] for key in dict_reflectors.keys() if key == reflector}


def replace_non_occurring_characters_and_uppercase(message, replacement_symbol):
    non_occurring_symbol = []

    if not replacement_symbol.isalpha():
        replacement_symbol = 'X'

    for symbol in message:
        if symbol not in non_occurring_symbol and not symbol.isalpha():
            non_occurring_symbol.append(symbol)

    for i in non_occurring_symbol:
        message = message.replace(i, replacement_symbol)

    return message.upper()


def set_rotors_initial_position(rotors, initial_position):
    alphabet = string.ascii_uppercase
    for index, rotor in enumerate(rotors.keys()):
        rotors[rotor] = rotors[rotor][alphabet.index(initial_position[index]):] +\
            rotors[rotor][0:alphabet.index(initial_position[index])]
    return rotors


def get_correct_rotors_steps(steps_rotors):
    correct_steps_rotors = []
    for i in range(0, len(steps_rotors) - 1):
        if steps_rotors[i] == 0 and steps_rotors[i + 1] != 0:
            correct_steps_rotors.append(1)
        else:
            correct_steps_rotors.append(steps_rotors[i])
    correct_steps_rotors.append(steps_rotors[len(steps_rotors) - 1])
    return correct_steps_rotors


def encrypt_enigma(message, list_rotors, reflector, replacement_symbol='X',
                   steps_rotors=(1, 1, 1), initial_position='AAA'):
    rotors_direct = set_rotors_initial_position(
        get_rotors(list_rotors), initial_position)
    rotors_reverse = {k: v for k, v in reversed(list(rotors_direct.items()))}

    rotors_direct_output = set_rotors_initial_position(
        get_rotors(list_rotors), initial_position)
    rotors_reverse_output = {k: v for k,
                             v in reversed(list(rotors_direct.items()))}

    reflector = get_reflector(reflector)
    message = replace_non_occurring_characters_and_uppercase(
        message, replacement_symbol)
    steps_rotors = get_correct_rotors_steps(steps_rotors)
    alphabet = string.ascii_uppercase

    encrypt_message = ''

    for symbol in message:
        for key in rotors_reverse.keys():
            symbol = rotors_reverse[key][alphabet.index(symbol)]
        for key in reflector.keys():
            if ''.join(reflector[key]).index(symbol) % 2 == 1:
                symbol = reflector[key][''.join(
                    reflector[key]).index(symbol) // 2][0]
            else:
                symbol = reflector[key][''.join(
                    reflector[key]).index(symbol) // 2][1]
        for key in rotors_direct.keys():
            symbol = alphabet[rotors_direct[key].index(symbol)]
        encrypt_message += symbol
        for index, key in enumerate(rotors_direct.keys()):
            rotors_direct[key] = rotors_direct[key][steps_rotors[index]                                                    :] + rotors_direct[key][0: steps_rotors[index]]
        rotors_reverse = {k: v for k, v in reversed(
            list(rotors_direct.items()))}

    print(f'Сообщение для зашифровки: {message}\n'
          f'Заменяющий символ: {replacement_symbol}\n'
          f'Роторы (прямой порядок): {rotors_direct_output}\n'
          f'Роторы (обратный порядок): {rotors_reverse_output}\n'
          f'Рефлектор: {reflector}\n'
          f'Шаги роторов: {steps_rotors}\n'
          f'Начальная позиция роторов: {initial_position}\n'
          f'Зашифрованное сообщение: {encrypt_message}\n')

    return encrypt_message


def decrypt_enigma(encrypt_message, list_rotors, reflector, steps_rotors, initial_position):
    rotors_direct = set_rotors_initial_position(
        get_rotors(list_rotors), initial_position)
    rotors_reverse = {k: v for k, v in reversed(list(rotors_direct.items()))}

    rotors_direct_output = set_rotors_initial_position(
        get_rotors(list_rotors), initial_position)
    rotors_reverse_output = {k: v for k,
                             v in reversed(list(rotors_direct.items()))}

    reflector = get_reflector(reflector)
    steps_rotors = get_correct_rotors_steps(steps_rotors)
    alphabet = string.ascii_uppercase

    decrypt_message = ''

    for symbol in encrypt_message:
        for key in rotors_reverse.keys():
            symbol = rotors_reverse[key][alphabet.index(symbol)]
        for key in reflector.keys():
            if ''.join(reflector[key]).index(symbol) % 2 == 1:
                symbol = reflector[key][''.join(
                    reflector[key]).index(symbol) // 2][0]
            else:
                symbol = reflector[key][''.join(
                    reflector[key]).index(symbol) // 2][1]
        for key in rotors_direct.keys():
            symbol = alphabet[rotors_direct[key].index(symbol)]
        decrypt_message += symbol
        for index, key in enumerate(rotors_direct.keys()):
            rotors_direct[key] = rotors_direct[key][steps_rotors[index]                                                    :] + rotors_direct[key][0: steps_rotors[index]]
            rotors_reverse = {k: v for k, v in reversed(
                list(rotors_direct.items()))}
    print(f'Сообщение для расшифровки: {encrypt_message}\n'
          f'Роторы (прямой порядок): {rotors_direct_output}\n'
          f'Роторы (обратный порядок): {rotors_reverse_output}\n'
          f'Рефлектор: {reflector}\n'
          f'Шаги роторов: {steps_rotors}\n'
          f'Начальная позиция роторов: {initial_position}\n'
          f'Расшифрованное сообщение: {decrypt_message}')
    return decrypt_message


def main():
    message = 'maksimleonidovichdashchinskii'
    list_rotors = ['IV', 'III', 'II']
    reflector = 'C Dunn'
    replacement_symbol = 'X'
    steps_rotors = [0, 0, 4]
    initial_position = 'AAA'

    print(f'----- Зашифровывание с помощью машины Энигма -----')
    encrypt_message = encrypt_enigma(message=message, list_rotors=list_rotors, reflector=reflector,
                                     replacement_symbol=replacement_symbol, steps_rotors=steps_rotors,
                                     initial_position=initial_position)

    print(f'----- Расшифровывание с помощью машины Энигма -----')
    decrypt_enigma(encrypt_message=encrypt_message, list_rotors=list_rotors, reflector=reflector,
                   steps_rotors=steps_rotors, initial_position=initial_position)


main()
