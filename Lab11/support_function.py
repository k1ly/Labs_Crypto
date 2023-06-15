import matplotlib.pyplot as plt


def read_file(name_file: str, size_buffer: int):
    file_for_only_read = open(name_file, 'r', encoding="utf8")
    return file_for_only_read.read() if size_buffer <= -1 else file_for_only_read.read()[:size_buffer]


def addition(message: str, value_l: int):
    rate = 1088

    possible_values_l = [1, 2, 3, 4, 5, 6]
    if value_l is None or value_l not in possible_values_l:
        value_l = 6

    message_bin = ''.join([(16 - len(bin(ord(i))[2:])) * '0' + bin(ord(i))[2:] for i in message])

    message_bin_add = message_bin + '1' + '0' * (rate - len(message_bin) % rate - 2) + '1'

    array_n = [message_bin_add[i * rate: (i + 1) * rate] for i in range(len(message_bin_add) // rate)]

    return array_n


def build_histogram(x, y):
    plt.figure(figsize=(9, 9))
    plt.bar(x, y)
    plt.title('Быстродействие алгоритма хеширования SHA-1')
    plt.xlabel('Длина сообщение')
    plt.ylabel('Время вычисления хеша')
    plt.show()
