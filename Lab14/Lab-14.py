from PIL import Image
from supp_function import open_image, extract_information


class Error(Exception):
    """Базовый класс для других исключений"""
    pass


class SmallImageSize(Error):
    """Вызывается, когда размеры фотографии маленькие"""
    pass


def encrypt(image_path: str, embedded_message: str, embedding_mode: int):
    try:
        rgb_image_np = open_image(image_path)

        size_image = rgb_image_np.shape[0:2]

        if len(embedded_message) > size_image[0] * size_image[1]:
            raise SmallImageSize

        rgb_image_np = rgb_image_np.reshape(
            (rgb_image_np.shape[0] * rgb_image_np.shape[1], 3))

        if embedding_mode == 1:
            for i in range(len(embedded_message)):
                rgb_image_np[i][2] = 1 & int(embedded_message[i])
        elif embedding_mode == 2:
            random_positions = extract_information(
                size_image, len(embedded_message))
            for i in range(len(embedded_message)):
                rgb_image_np[random_positions[i]][2] = 1 & int(
                    embedded_message[i])
        rgb_image_np = rgb_image_np.reshape((size_image[0], size_image[1], 3))
        new_image = Image.fromarray(rgb_image_np, 'RGB')
        encrypted_image_path = R"D:\University_BSTU\Labs\КМЗИ\Лабы\Lab-14\encrypted.png"
        new_image.save(encrypted_image_path)
        return len(embedded_message)
    except SmallImageSize:
        print(f'Размеры изображения малы для встраивания')
        return 0


def decrypt(image_path: str, len_embedded_message: int, embedding_mode: int):
    rgb_image_np = open_image(image_path)

    size_image = rgb_image_np.shape[0:2]

    rgb_image_np = rgb_image_np.reshape(
        (rgb_image_np.shape[0] * rgb_image_np.shape[1], 3))

    decrypt_binary_message = ''
    if embedding_mode == 1:
        for i in range(len_embedded_message):
            decrypt_binary_message += str(rgb_image_np[i][2] & 1)
    elif embedding_mode == 2:
        random_positions = extract_information(
            size_image, len_embedded_message)
        for i in random_positions:
            decrypt_binary_message += str(rgb_image_np[i][2] & 1)
    decrypt_message = ''.join([chr(int(decrypt_binary_message[i * 16: (i + 1) * 16], 2))
                               for i in range(len(decrypt_binary_message) // 16)])
    return decrypt_message


def get_LSB(file_for_shades: str):
    rgb_image_np = open_image(file_for_shades)
    size_image = rgb_image_np.shape[0], rgb_image_np.shape[1]

    rgb_image_np_red = rgb_image_np.copy().reshape(
        (rgb_image_np.shape[0] * rgb_image_np.shape[1], 3))
    rgb_image_np_green = rgb_image_np.copy().reshape(
        (rgb_image_np.shape[0] * rgb_image_np.shape[1], 3))
    rgb_image_np_blue = rgb_image_np.copy().reshape(
        (rgb_image_np.shape[0] * rgb_image_np.shape[1], 3))
    rgb_image_np_rgb = rgb_image_np.copy().reshape(
        (rgb_image_np.shape[0] * rgb_image_np.shape[1], 3))

    for i in range(rgb_image_np.shape[0] * rgb_image_np.shape[1]):
        current_red_LSB = rgb_image_np_red[i][0] & 1
        rgb_image_np_red[i] = list(
            map(lambda x: x * current_red_LSB, [255, 255, 255]))
        current_green_LSB = rgb_image_np_green[i][1] & 1
        rgb_image_np_green[i] = list(
            map(lambda x: x * current_green_LSB, [255, 255, 255]))
        current_blue_LSB = rgb_image_np_blue[i][2] & 1
        rgb_image_np_blue[i] = list(
            map(lambda x: x * current_blue_LSB, [255, 255, 255]))

        rgb_image_np_rgb[i] = rgb_image_np_red[i][0], rgb_image_np_green[i][1], rgb_image_np_blue[i][2]

    rgb_image_np_red = rgb_image_np_red.reshape(
        (size_image[0], size_image[1], 3))
    rgb_image_np_green = rgb_image_np_green.reshape(
        (size_image[0], size_image[1], 3))
    rgb_image_np_blue = rgb_image_np_blue.reshape(
        (size_image[0], size_image[1], 3))
    rgb_image_np_rgb = rgb_image_np_rgb.reshape(
        (size_image[0], size_image[1], 3))

    new_image_red = Image.fromarray(rgb_image_np_red, 'RGB')
    new_image_green = Image.fromarray(rgb_image_np_green, 'RGB')
    new_image_blue = Image.fromarray(rgb_image_np_blue, 'RGB')
    new_image_rgb = Image.fromarray(rgb_image_np_rgb, 'RGB')

    encrypted_image_path_red = R"D:\University_BSTU\Labs\КМЗИ\Лабы\Lab-14\red_shades.png"
    encrypted_image_path_green = R"D:\University_BSTU\Labs\КМЗИ\Лабы\Lab-14\green_shades.png"
    encrypted_image_path_blue = R"D:\University_BSTU\Labs\КМЗИ\Лабы\Lab-14\blue_shades.png"
    encrypted_image_path_rgb = R"D:\University_BSTU\Labs\КМЗИ\Лабы\Lab-14\rgb_shades.png"

    new_image_red.save(encrypted_image_path_red)
    new_image_green.save(encrypted_image_path_green)
    new_image_blue.save(encrypted_image_path_blue)
    new_image_rgb.save(encrypted_image_path_rgb)


def task_1():
    message = open('text.txt', 'r', encoding='utf8').read()[:100]

    embedded_message = ''.join(
        [bin(ord(i))[2:].rjust(16, '0') for i in message])

    file_for_embedding = R"embedded_image.jpg"
    file_to_readout = R"D:\University_BSTU\Labs\КМЗИ\Лабы\Lab-14\encrypted.png"

    len_embedded_message = encrypt(file_for_embedding, embedded_message, 1)
    decrypt_message = decrypt(file_to_readout, len_embedded_message, 1)

    print(f'----- Встраивомое сообщение -----\n{message}\n'
          f'----- Считанное сообщение -----\n{decrypt_message}\n'
          f'----- Сообщение считано {"верно!" if message == decrypt_message else "не верно!"} -----')


def task_2():
    file_for_shades = R"embedded_image.jpg"
    get_LSB(file_for_shades)


def task_3():
    message = open('text.txt', 'r', encoding='utf8').read()[:100]

    embedded_message = ''.join(
        [bin(ord(i))[2:].rjust(16, '0') for i in message])

    file_for_embedding = R"embedded_image.jpg"
    file_to_readout = R"D:\University_BSTU\Labs\КМЗИ\Лабы\Lab-14\encrypted.png"

    len_embedded_message = encrypt(file_for_embedding, embedded_message, 2)
    decrypt_message = decrypt(file_to_readout, len_embedded_message, 2)

    print(f'----- Встраиваемое сообщение -----\n{message}\n'
          f'----- Считанное сообщение -----\n{decrypt_message}\n'
          f'----- Сообщение считано {"верно!" if message == decrypt_message else "не верно!"} -----')


def main():
    task_1()
    task_2()
    task_3()


if __name__ == '__main__':
    main()
