import random
from support_function import InverseNumber


alphabet = {'А': (189, 297), 'Б': (189, 454), 'В': (192, 32), 'Г': (192, 719),
            'Д': (194, 205), 'Е': (194, 546), 'Ж': (197, 145), 'З': (197, 606),
            'И': (198, 224), 'Й': (198, 527), 'К': (200, 30), 'Л': (200, 721),
            'М': (203, 324), 'Н': (203, 427), 'О': (205, 372), 'П': (205, 379),
            'Р': (206, 106), 'С': (206, 645), 'Т': (209, 82), 'У': (209, 669),
            'Ф': (210, 31), 'Х': (210, 720), 'Ц': (215, 247), 'Ч': (215, 504),
            'Ш': (218, 601), 'Щ': (218, 601), 'Ъ': (221, 138), 'Ы': (221, 613),
            'Ь': (226, 9), 'Э': (226, 742), 'Ю': (227, 299), 'Я': (227, 452),
            }

inverse_alphabet = {alphabet[key]: key for key in alphabet.keys()}


class EllipticCurve:
    points = []

    def __init__(self, a, b, p):
        self.a = a  # Коэффициент a уравнения кривой
        self.b = b  # Коэффициент b уравнения кривой
        self.p = p  # Простое число, определяющее модуль

    def get_points_by_range(self, a, b):
        if b >= self.p:
            b = self.p

        list_remains = []
        for i in range(a, b):
            list_remains.append(pow(i, 2, self.p))

        list_square_roots = []
        for i in range(a, b):
            list_square_roots.append((i ** 3 + self.a * i + self.b) % self.p)

        list_points = []
        for x, i in enumerate(list_square_roots):
            if i in list_remains:
                if i != 0:
                    list_points += list((x + a, a + index)
                                        for index, j in enumerate(list_remains) if j == i)
        return list_points

    def add_points_by_range(self, a, b):
        self.points += self.get_points_by_range(a, b)

    def is_point_on_curve(self, point):
        return (point[1] ** 2) % self.p == (point[0] ** 3 + self.a * point[0] + self.b) % self.p

    def point_addition(self, point_1, point_2):
        if point_1[0] == point_2[0] and point_1[1] == point_2[1]:
            s = (3 * (point_1[0] ** 2) + self.a) * \
                pow(2 * point_1[1], -1, self.p) % self.p
        else:
            s = (point_2[1] - point_1[1]) * \
                pow(point_2[0] - point_1[0], -1, self.p) % self.p
        x3 = (s ** 2 - point_1[0] - point_2[0]) % self.p
        y3 = (s * (point_1[0] - x3) - point_1[1]) % self.p
        return x3, y3

    def point_multiplication(self, point, n):
        result_x = None
        result_y = None
        current_x = point[0]
        current_y = point[1]
        while n > 0:
            if n & 1 == 1:
                if result_x is None:
                    result_x = current_x
                    result_y = current_y
                else:
                    result_x, result_y = self.point_addition(
                        (result_x, result_y), (current_x, current_y))
            current_x, current_y = self.point_addition(
                (current_x, current_y), (current_x, current_y))
            n >>= 1
        return result_x, result_y

    def point_difference(self, point_1, point_2):
        return self.point_addition(point_1, (point_2[0], -point_2[1]))


def task_1():
    curve = EllipticCurve(-1, 1, 751)
    a = 0
    b = 750
    curve.add_points_by_range(a, b)
    a = 106
    b = 140

    k = 9
    r = 7
    P = (56, 332)
    Q = (69, 241)
    R = (83, 373)
    print(f'----- Задание 1. Нахождение точек на диапазоне и операции с точками -----\n'
          f'--- 1.1 --- Точки на ЭК E751(-1, 1) в диапазоне {a, b}: {curve.get_points_by_range(a, b)}\n'
          f'Количество точек в диапазоне {a, b}: {len(curve.get_points_by_range(a, b))}\n'
          f'--- 1.2 ---\n'
          f'а) kР = {curve.point_multiplication(P, k)}\n'
          f'б) P + Q = {curve.point_addition(P, Q)}\n'
          f'в) kP + rQ - R = {curve.point_difference(curve.point_addition(curve.point_multiplication(P, k), curve.point_multiplication(Q, r)), R)}\n'
          f'г) Р – Q + R = {curve.point_addition(curve.point_difference(P, Q), R)}')


def EncryptByEC(message: str):
    curve = EllipticCurve(-1, 1, 751)
    message_EC = [alphabet[i] for i in message.upper()]

    G = (0, 1)
    d = 12
    Q = curve.point_multiplication(G, d)
    k = int(random.random() * curve.p)

    # Зашифровывание
    encrypt_message_EC = []
    for i in message_EC:
        c_1 = curve.point_multiplication(G, k)
        c_2 = curve.point_addition(i, curve.point_multiplication(Q, k))
        encrypt_message_EC.append((c_1, c_2))

    # Расшифровывание
    decrypt_message_EC = []
    decrypt_message = ''
    for i in encrypt_message_EC:
        m = curve.point_difference(i[1], curve.point_multiplication(i[0], d))
        decrypt_message_EC.append(m)
        decrypt_message += inverse_alphabet[m]

    print(f'\n----- Задание 2.  Зашифровывание/расшифровывание информации с помощью ЭК -----\n'
          f'G = {G}\n'
          f'd = {d}\n'
          f'Q = {Q}\n'
          f'k = {k}\n'
          f'Сообщение: {message}\n'
          f'Сообщение ЭК: {message_EC}\n'
          f'ЭК имеет вид: \n'
          f'Зашифрованное сообщение ЭК: {encrypt_message_EC}\n'
          f'Расшифрованное сообщение ЭК: {decrypt_message_EC}\n'
          f'Расшифрованное сообщение: {decrypt_message}\n')

    pass


def EDSBasedOnEC(message: str):
    curve = EllipticCurve(-1, 1, 751)

    G = (416, 55)
    q = 13

    s = 0
    r = 0
    u_1 = 0
    u_2 = 0
    while s == 0 or r == 0 or u_1 == 0 or u_2 == 0:
        d = 12

        k = 8

        Q = curve.point_multiplication(G, d)

        # Отправитель
        r = curve.point_multiplication(G, k)[0] % curve.p
        t = InverseNumber(k, q)[1] % q

        hash_message_sender = alphabet[message[0].upper()][0] % 13
        s = (t * (hash_message_sender + d * r)) % q

        # Получатель
        result_condition_fulfillment = r > 1 and s < q
        hash_recipient = alphabet[message[0].upper()][0] % 13
        w = InverseNumber(s, q)[1] % q
        u_1 = pow(w * hash_recipient, 1, q)
        u_2 = pow(w * r, 1, q)

        v = curve.point_addition(curve.point_multiplication(
            G, u_1), curve.point_multiplication(Q, u_2))[0]
        result_verification = r == v

    print(f'----- Задание 3. Генерация ЭЦП на основе ECDSA -----\n'
          f'G = {G}\n'
          f'q = {q}\n'
          f'd = {d}\n'
          f'k = {k}\n'
          f'Q = {Q}\n'
          f'r = {r}\n'
          f't = {t}\n'
          f'H(message) = {hash_message_sender}\n'
          f's = {s}\n'
          f'Отправлено {message} и ЭЦП({r, s})\n')

    print(f'Условие 1 < r, s < q {"выполняется!" if result_condition_fulfillment else "не выполняется!"}\n'
          f'Хеш получателя = {hash_recipient}\n'
          f'w = {w}\n'
          f'u_1 = {u_1}\n'
          f'u_2 = {u_2}\n'
          f'v = {v}\n'
          f'Сравниваем v и r, т.е. {v} и {r}\n'
          f'Подпись верифицирована {"успешно!" if result_verification else "не успешно!"}')
    pass


def main():
    task_1()
    message = 'ДащинскийМаксимЛеонидович'
    EncryptByEC(message)
    EDSBasedOnEC(message)


main()
