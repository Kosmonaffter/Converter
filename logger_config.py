import logging


def setup_logger():
    logger = logging.getLogger('bmp_ico_logger')
    logger.setLevel(logging.DEBUG)

    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.DEBUG)
    # Формат вывода сообщений в консоль
    formatter = logging.Formatter(
        '[%(asctime)s] %(levelname)s - %(message)s',
        '%Y-%m-%d %H:%M:%S')
    console_handler.setFormatter(formatter)
    # Добавляем обработчик к логгеру
    logger.addHandler(console_handler)
    # Отключаем, чтобы не дублировались логи, если есть root-логгер
    logger.propagate = False

    return logger
