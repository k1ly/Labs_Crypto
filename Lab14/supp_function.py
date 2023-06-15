from PIL import Image
import numpy as np


def open_image(filename: str):
    if filename:
        image = Image.open(filename)
        img_rgb = image.convert('RGB')
        rgb_image_np = np.copy(img_rgb)
        return rgb_image_np


def extract_information(list_image, count_number: int):
    a = list_image[0] + 19
    b = list_image[1] + 19
    current_x = 3
    n = list_image[0] * list_image[1]

    random_numbers = []
    for i in range(count_number):
        current_x = (a * current_x + b) % n
        random_numbers.append(current_x)
    return random_numbers
