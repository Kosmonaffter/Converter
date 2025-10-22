import os
import tkinter as tk
from pathlib import Path
from tkinter import filedialog, messagebox, ttk

import backend
from logger_config import setup_logger

logger = setup_logger()


class Converter(tk.Tk):
    'Основной класс GUI приложения на tkinter.'

    def __init__(self):
        super().__init__()
        style = ttk.Style()
        style.theme_use('clam')
        self.attributes('-alpha', 0.9)

        # Иконка и заголовок
        try:
            self.iconbitmap('icon/Icon_apps.ico')
        except Exception as e:
            logger.warning(f'Не удалось загрузить иконку: {e}')

        self.title('Конвертер файлов изображений')
        self.is_maximized = False

        self.last_save_dir = str(Path.home())
        self.last_open_dir = str(Path.home())

        self.file_path_var = tk.StringVar()
        self.save_path_var = tk.StringVar()
        self.format_var = tk.StringVar()

        # Переменные для выбора размеров ICO
        self.size_16_var = tk.BooleanVar(value=False)
        self.size_32_var = tk.BooleanVar(value=False)
        self.size_48_var = tk.BooleanVar(value=False)
        self.size_64_var = tk.BooleanVar(value=False)
        self.size_128_var = tk.BooleanVar(value=False)
        self.size_256_var = tk.BooleanVar(value=False)

        self.supported_formats = {
            '.bmp': ['ICO', 'PNG', 'JPEG'],
            '.png': ['ICO', 'BMP', 'JPEG'],
            '.jpg': ['ICO', 'BMP', 'PNG'],
            '.jpeg': ['ICO', 'BMP', 'PNG'],
        }

        # Создаем Notebook для вкладок
        self.notebook = ttk.Notebook(self)
        self.notebook.pack(expand=True, fill='both', padx=10, pady=10)

        # Вкладка конвертера
        self.tab_converter = ttk.Frame(self.notebook)
        self.notebook.add(self.tab_converter, text='Конвертер')

        # Вкладка About
        self.tab_about = ttk.Frame(self.notebook)
        self.notebook.add(self.tab_about, text='О программе')

        self._create_converter_tab()
        self._create_about_tab()

    def _create_converter_tab(self):
        'Создает вкладку конвертера.'
        # Строка выбора файла
        tk.Label(
            self.tab_converter,
            text='Выберите файл:',
        ).grid(row=0, column=0, padx=5, pady=5, sticky='w')

        ttk.Entry(
            self.tab_converter,
            textvariable=self.file_path_var,
            width=50,
        ).grid(row=0, column=1, padx=5, pady=5, columnspan=2)

        ttk.Button(
            self.tab_converter,
            text='Обзор...',
            command=self.select_file,
        ).grid(row=0, column=3, padx=5, pady=5)

        # Строка выбора формата
        tk.Label(
            self.tab_converter,
            text='Выберите формат:',
        ).grid(row=1, column=0, padx=5, pady=5, sticky='w')

        self.format_combo = ttk.Combobox(
            self.tab_converter,
            state='readonly',
            textvariable=self.format_var,
            values=[],
            width=47,
        )
        self.format_combo.grid(
            row=1,
            column=1,
            padx=5,
            pady=5,
            columnspan=2,
        )
        self.format_combo.bind('<<ComboboxSelected>>', self.on_format_change)

        # Фрейм для выбора размеров ICO
        self.ico_frame = ttk.LabelFrame(
            self.tab_converter,
            text='Выберите размеры для ICO:',
        )
        self.ico_frame.grid(
            row=2,
            column=0,
            columnspan=4,
            padx=5,
            pady=5,
            sticky='we',
        )
        self.ico_frame.grid_remove()

        # Чекбоксы для размеров ICO
        ico_sizes = [
            ('16x16', self.size_16_var, 0, 0),
            ('32x32', self.size_32_var, 0, 1),
            ('48x48', self.size_48_var, 0, 2),
            ('64x64', self.size_64_var, 1, 0),
            ('128x128', self.size_128_var, 1, 1),
            ('256x256', self.size_256_var, 1, 2),
        ]

        for text, var, row, col in ico_sizes:
            ttk.Checkbutton(
                self.ico_frame,
                text=text,
                variable=var,
            ).grid(row=row, column=col, padx=10, pady=2, sticky='w')

        # Кнопки управления размерами
        ttk.Button(
            self.ico_frame,
            text='Выбрать все',
            command=self.select_all_sizes,
        ).grid(row=2, column=0, padx=10, pady=5, sticky='w')

        ttk.Button(
            self.ico_frame,
            text='Сбросить',
            command=self.deselect_all_sizes,
        ).grid(row=2, column=1, padx=10, pady=5, sticky='w')

        # Строка пути сохранения
        tk.Label(
            self.tab_converter,
            text='Путь для сохранения:',
        ).grid(row=3, column=0, padx=5, pady=5, sticky='w')

        ttk.Entry(
            self.tab_converter,
            textvariable=self.save_path_var,
            width=50,
        ).grid(row=3, column=1, padx=5, pady=5, columnspan=2)

        ttk.Button(
            self.tab_converter,
            text='Обзор...',
            command=self.select_save,
        ).grid(row=3, column=3, padx=5, pady=5)

        # Кнопка конвертации
        ttk.Button(
            self.tab_converter,
            text='Конвертировать',
            command=self.convert,
        ).grid(row=4, column=1, columnspan=2, pady=10)

        self.footer_label = tk.Label(
            self.tab_converter,
            text='@2025 kosmonaffter@yandex.ru',
            font=('Arial', 8),
            foreground='red',
        )
        self.footer_label.grid(
            row=5,
            column=0,
            columnspan=4,
            sticky='w',
            padx=5,
            pady=5,
        )

        # Настраиваем колонки для растягивания
        self.tab_converter.columnconfigure(1, weight=1)

    def _create_about_tab(self):
        'Создает вкладку О программе.'
        about_text = (
            'ConvertImagesTransparent\n\n'
            'Приложение для конвертации изображений '
            'между различными форматами.\n\n'
            'Поддерживаемые форматы:\n'
            '• Входные: PNG, JPG, JPEG, BMP, ICO\n'
            '• Выходные: ICO, PNG, BMP, JPEG\n\n'
            'Особенности ICO:\n'
            '• Выбор нужных размеров иконки\n'
            '• Поддержка размеров от 16x16 до 256x256\n'
            '• Интеллектуальная конвертация из любых форматов\n\n'
            'Автор: Telegram: @kosmonafftsb\n'
            'Email: kosmonaffter@yandex.ru\n'
            '© 2025'
        )

        label_about = ttk.Label(
            self.tab_about,
            text=about_text,
            justify='left',
            font=('Arial', 11),
            padding=20,
            anchor='nw',
        )
        label_about.pack(expand=True, fill='both')

    def on_format_change(self, event=None):
        'Обработчик изменения выбранного формата.'
        selected_format = self.format_var.get().upper()

        if selected_format == 'ICO':
            self.ico_frame.grid()
        else:
            self.ico_frame.grid_remove()

    def select_all_sizes(self):
        'Выбирает все размеры ICO.'
        size_vars = [
            self.size_16_var,
            self.size_32_var,
            self.size_48_var,
            self.size_64_var,
            self.size_128_var,
            self.size_256_var,
        ]
        for var in size_vars:
            var.set(True)

    def deselect_all_sizes(self):
        'Сбрасывает все размеры ICO.'
        size_vars = [
            self.size_16_var,
            self.size_32_var,
            self.size_48_var,
            self.size_64_var,
            self.size_128_var,
            self.size_256_var,
        ]
        for var in size_vars:
            var.set(False)

    def get_selected_ico_sizes(self):
        'Возвращает список выбранных размеров для ICO.'
        sizes = []
        if self.size_16_var.get():
            sizes.append((16, 16))
        if self.size_32_var.get():
            sizes.append((32, 32))
        if self.size_48_var.get():
            sizes.append((48, 48))
        if self.size_64_var.get():
            sizes.append((64, 64))
        if self.size_128_var.get():
            sizes.append((128, 128))
        if self.size_256_var.get():
            sizes.append((256, 256))

        if not sizes:
            sizes = [(16, 16), (32, 32), (48, 48)]
            messagebox.showwarning(
                'Внимание',
                'Не выбран ни один размер ICO. '
                'Используются размеры по умолчанию: 16x16, 32x32, 48x48',
            )

        return sizes

    def select_file(self):
        path = filedialog.askopenfilename(
            initialdir=self.last_open_dir,
            filetypes=[
                ('Изображения', '*.png *.jpg *.jpeg *.bmp *.ico'),
                ('Все файлы', '*.*'),
            ],
        )
        if path:
            self.file_path_var.set(path)
            self.last_open_dir = str(Path(path).parent)
            ext = Path(path).suffix.lower()
            logger.debug(f'Выбран файл: {path} с расширением: {ext}')

            formats = self.supported_formats.get(ext, [])
            if not formats:
                messagebox.showwarning(
                    'Внимание',
                    f'Расширение {ext} не поддерживается.',
                )
                self.format_combo['values'] = []
                self.format_var.set('')
                self.ico_frame.grid_remove()
            else:
                self.format_combo['values'] = formats
                self.format_combo.current(0)
                logger.debug(f'Доступные форматы: {formats}')
                self.on_format_change()

    def select_save(self):
        selected_format = self.format_var.get().lower()
        def_ext = '.' + selected_format if selected_format else ''

        path = filedialog.asksaveasfilename(
            initialdir=self.last_save_dir,
            defaultextension=def_ext,
            filetypes=[(f'{selected_format.upper()} файлы', def_ext)]
            if def_ext else [],
        )
        if path:
            p = Path(path)
            path = str(p.with_suffix(def_ext))
            self.save_path_var.set(path)
            self.last_save_dir = str(p.parent)
            logger.debug(f'Выбран путь сохранения: {path}')

    def convert(self):
        input_path = Path(self.file_path_var.get()).expanduser().resolve()
        output_path = Path(self.save_path_var.get()).expanduser().resolve()
        format_out = self.format_var.get().upper()

        logger.debug(
            f'Начинаем конвертацию: '
            f'{input_path} -> {output_path}, в {format_out}'
        )

        if not input_path.exists() or not input_path.is_file():
            logger.error('Входной файл не найден')
            messagebox.showerror('Ошибка', 'Входной файл не найден!')
            return

        if not format_out:
            logger.warning('Формат не выбран')
            messagebox.showwarning('Ошибка', 'Выберите формат!')
            return

        if not output_path.parent.exists():
            try:
                os.makedirs(output_path.parent)
                logger.debug(f'Создана папка: {output_path.parent}')
            except Exception as e:
                logger.error(f'Ошибка создания папки: {e}')
                messagebox.showerror(
                    'Ошибка',
                    f'Не удалось создать папку: {e}',
                )
                return

        try:
            if format_out == 'ICO':
                ico_sizes = self.get_selected_ico_sizes()
                logger.debug(f'Выбранные размеры ICO: {ico_sizes}')
                backend.convert_image_format(
                    str(input_path),
                    str(output_path),
                    format_out,
                    ico_sizes,
                )
            else:
                backend.convert_image_format(
                    str(input_path),
                    str(output_path),
                    format_out,
                )

            logger.info(f'Успешно сконвертировано: {output_path}')
            messagebox.showinfo('Успех', f'Файл сохранён: {output_path}')
            self.save_path_var.set('')
            self.file_path_var.set('')
        except Exception as e:
            logger.error(f'Ошибка конвертации: {e}', exc_info=True)
            messagebox.showerror('Ошибка', f'Ошибка конвертации: {e}')


if __name__ == '__main__':
    app = Converter()
    app.mainloop()
