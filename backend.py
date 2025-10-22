from PIL import Image


def convert_image_format(
        input_path, output_path,
        output_format,
        ico_sizes=None
):
    '''
    Универсальная конвертация изображений
    с поддержкой выбора размеров для ICO.

    Args:
        input_path (str): Путь к исходному файлу.
        output_path (str): Путь для сохранения результата.
        output_format (str): Формат выходного файла.
        ico_sizes (list): Список кортежей с размерами для ICO файла.
    '''
    if ico_sizes is None:
        ico_sizes = [(16, 16), (32, 32), (48, 48)]

    with Image.open(input_path) as img:
        # Для JPEG убираем альфа-канал
        if output_format.upper() == 'JPEG' and img.mode in ('RGBA', 'LA'):
            img = img.convert('RGB')

        # Обработка ICO с выбранными размерами
        if output_format.upper() == 'ICO':
            # Если исходник не BMP или PNG, конвертируем в PNG в памяти
            if img.format not in ('BMP', 'PNG'):
                from io import BytesIO

                temp = BytesIO()
                img.save(temp, format='PNG')
                temp.seek(0)
                with Image.open(temp) as png_img:
                    png_img.save(
                        output_path,
                        format='ICO',
                        sizes=ico_sizes,
                    )
                return

            # Если BMP или PNG - сохраняем сразу в ICO
            img.save(
                output_path,
                format='ICO',
                sizes=ico_sizes,
            )
        else:
            # Для других форматов просто сохраняем
            img.save(output_path, format=output_format)


def get_default_ico_sizes():
    'Возвращает размеры ICO по умолчанию.'
    return [(16, 16), (32, 32), (48, 48)]
