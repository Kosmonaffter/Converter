import tkinter as tk
from tkinter import filedialog, messagebox
from pathlib import Path
import os

from backend import convert_bmp_to_ico
from logger_config import setup_logger

# Инициализация логгера, который пишет в файл app.log
logger = setup_logger()


class Converter(tk.Tk):
    """Основной класс графического приложения на tkinter"""

    def __init__(self):
        super().__init__()
        # Заголовок окна
        self.title('Конвертер BMP в ICO')

        # Переменные, связывающие поля ввода с данными
        self.bmp_path_var = tk.StringVar()
        self.save_path_var = tk.StringVar()

        # Метка рядом с полем выбора BMP файла
        tk.Label(self, text="Выберите BMP файл:").grid(
            row=0, column=0, padx=5, pady=5
        )
        # Поле для отображения или ввода пути к BMP файлу
        tk.Entry(self, textvariable=self.bmp_path_var, width=50).grid(
            row=0, column=1, padx=5, pady=5
        )
        # Кнопка для открытия диалога выбора BMP файла
        tk.Button(self, text="Обзор...", command=self.select_bmp).grid(
            row=0, column=2, padx=5, pady=5
        )

        # Метка рядом с полем для выбора пути сохранения ICO
        tk.Label(self, text="Путь для сохранения ICO:").grid(
            row=1, column=0, padx=5, pady=5
        )
        # Поле для отображения или ввода пути сохранения ICO
        tk.Entry(self, textvariable=self.save_path_var, width=50).grid(
            row=1, column=1, padx=5, pady=5
        )
        # Кнопка для открытия диалога выбора пути сохранения
        tk.Button(self, text="Обзор...", command=self.select_save).grid(
            row=1, column=2, padx=5, pady=5
        )

        # Кнопка для запуска процесса конвертации
        tk.Button(self, text="Конвертировать", command=self.convert).grid(
            row=2, column=1, pady=10
        )

    def select_bmp(self):
        """
        Открывает диалог выбора файла BMP.
        Если файл выбран - обновляет переменную и пишет в лог.
        """
        path = filedialog.askopenfilename(
            initialdir=str(Path.home()),  # Начальная папка-домашняя польз.
            filetypes=[("BMP файлы", "*.bmp")]  # Фильтр по расширению
        )
        if path:
            self.bmp_path_var.set(path)  # Заполняем поле ввода выбранным путём
            logger.debug(f"Выбран BMP файл: {path}")  # Запись в лог

    def select_save(self):
        """
        Диалог выбора пути и имени для сохранения ICO.
        Аналогично обновляет поле и лог.
        """
        path = filedialog.asksaveasfilename(
            initialdir=str(Path.home()),  # Начальная папка домашняя
            defaultextension=".ico",  # Дополнение расширения ICO
            filetypes=[("ICO файлы", "*.ico")],  # Фильтр по ICO
        )
        if path:
            self.save_path_var.set(path)  # Заполнение поля
            logger.debug(f"Выбран путь сохранения ICO: {path}")  # Запись в лог

    def convert(self):
        """
        Выполняется по нажатию кнопки «Конвертировать».
        1. Получает и нормализует пути через pathlib.
        2. Проверяет наличие исходного файла и папки для сохранения.
        3. Создаёт папку, если не существует.
        4. Запускает конвертацию.
        5. Логирует подробности и показывает диалоги.
        """
        bmp_path = Path(self.bmp_path_var.get()).expanduser().resolve()
        save_path = Path(self.save_path_var.get()).expanduser().resolve()

        logger.debug(f"Попытка конвертации BMP: {bmp_path}")
        logger.debug(f"Путь сохранения ICO: {save_path}")

        # Проверка, что BMP файл существует
        if not bmp_path.exists() or not bmp_path.is_file():
            logger.error("Исходный BMP файл не найден или путь неправильный")
            messagebox.showerror("Ошибка", "Исходный BMP файл не найден!")
            return

        # Если папка для сохранения ICO не существует - создаём её
        if not save_path.parent.exists():
            logger.warning(f"Папка {save_path.parent} не найдена, создаём")
            try:
                os.makedirs(save_path.parent)
            except Exception as error:
                logger.error(f"Не удалось создать папку: {error}")
                messagebox.showerror(
                    "Ошибка",
                    f"Не удалось создать папку для сохранения: {error}",
                )
                return

        # Конвертация BMP в ICO с логированием результата
        try:
            convert_bmp_to_ico(str(bmp_path), str(save_path))
            logger.info(f"Конвертация успешна: {save_path}")
            messagebox.showinfo(
                "Успех",
                f"Файл успешно сохранён как {save_path}"
            )
        except Exception as error:
            logger.error(f"Ошибка конвертации: {error}", exc_info=True)
            messagebox.showerror("Ошибка", f"Ошибка конвертации: {error}")


# Запускаем приложение, если скрипт выполняется напрямую
if __name__ == "__main__":
    app = Converter()
    app.mainloop()
