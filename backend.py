# Импортируем класс Image из библиотеки Pillow для работы с изображениями
from PIL import Image


def convert_bmp_to_ico(input_path, output_path):
    """
    Конвертирует BMP файл в ICO с несколькими стандартными размерами.
    input_path: путь к входному BMP файлу
    output_path: путь для сохранения ICO
    """
    bmp_image = Image.open(input_path)  # Открываем BMP изображение
    bmp_image.save(
        output_path,
        format='ICO',  # Сохраняем как ICO
        sizes=[
            (16, 16),
            (32, 32),
            (48, 48),
            (64, 64),
            (128, 128),
        ]
    )  # Стандартные размеры иконок
