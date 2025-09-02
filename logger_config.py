import logging
from logging.handlers import RotatingFileHandler


def setup_logger():
    logger = logging.getLogger('bmp_ico_logger')
    logger.setLevel(logging.DEBUG)

    # Ротация файла лога размером 1 МБ, максимум 100 файлов
    handler = RotatingFileHandler(
        'app.log',
        maxBytes=1_000_000,   # 1 MB
        backupCount=100,
        encoding='utf-8'
    )

    formatter = logging.Formatter(
        '[%(asctime)s] %(levelname)s - %(message)s',
        '%Y-%m-%d %H:%M:%S')
    handler.setFormatter(formatter)

    logger.addHandler(handler)
    return logger
