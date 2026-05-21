import tkinter as tk
from tkinter import messagebox
import math
try:
    from tkmacosx import Button
except ImportError:
    from tkinter import Button
import os

# Основная функция
def start_calculator():
    memory = {'val': 0.0}

    # Главное окно
    window = tk.Tk()
    window.title("Инженерный калькулятор")
    window.geometry("350x790")
    window.configure(bg='#2C3E50')

    # Цветовая палитра
    THEME_DARK = {
        'bg': '#2C3E50', 'disp': '#34495E', 'text': '#ECF0F1',
        'num': '#5D6D7E', 'op': '#E67E22', 'spec': '#95A5A6', 'math': '#27AE60'
    }
    THEME_LIGHT = {
        'bg': '#E5E5EA', 'disp': '#FFFFFF', 'text': '#1C1C1E',
        'num': '#D1D1D6', 'op': '#FF9500', 'spec': '#AEB1B8', 'math': '#34C759'
    }

    is_dark_theme = True
    dislpay_var = tk.StringVar()
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    HISTORY_PATH = os.path.join(BASE_DIR, 'history.txt')

    COLOR_BG = THEME_DARK['bg']
    COLOR_DISPLAY = THEME_DARK['disp']
    COLOR_TEXT = THEME_DARK['text']
    COLOR_BTN_NUM = THEME_DARK['num']
    COLOR_BTN_OP = THEME_DARK['op']
    COLOR_BTN_SPEC = THEME_DARK['spec']
    COLOR_BTN_MATH = THEME_DARK['math']

    window.configure(bg=COLOR_BG)

    # Функции логики

    # Сохраниние истории вычеслении
    def save_to_file(expression, result):
        try:
            with open(HISTORY_PATH, 'a', encoding='utf-8') as file:
                file.write(f'{expression} = {result}\n')
            print(f'УСПЕХ: В файл записано -> {expression} = {result}')
        except Exception as e:
            print(f'ОШИБКА ЗАПИСИ В ФАЙЛ: {e}')

    # Окно для отображения истории из файла
    def show_history():

        def load_from_history(event):
            selection = history_listbox.curselection()
            if not selection: return

            selected_text = history_listbox.get(selection[0])
            expression = selected_text.split(' = ')[0]

            display.delete(0, tk.END)
            display.insert(0, expression)
            h_win.destroy()
            print(f'Загружено из истории: {expression}')

        def clear_txt_file():
            with open(HISTORY_PATH, 'w', encoding='utf-8') as f:
                pass
            history_listbox.delete(0, tk.END)
            print('Файл истории полностью очищен!')

        try:
            if not os.path.exists(HISTORY_PATH):
                print('Файла истории нет по пути:', HISTORY_PATH)
                messagebox.showinfo('!', 'Пусто')
                return

            with open(HISTORY_PATH, 'r', encoding='utf-8') as file:
                lines = file.readlines()
            h_win = tk.Toplevel(window)
            h_win.title('История')
            h_win.geometry('250x450')
            h_win.configure(bg=COLOR_BG)
            history_listbox = tk.Listbox(h_win, bg=COLOR_DISPLAY, fg=COLOR_TEXT, font=('Arial', 14),
                                         borderwidth=0, highlightthickness=0)
            history_listbox.pack(fill='both', expand=True, padx=10, pady=10)
            for line in lines:
                if line.strip():
                    history_listbox.insert(tk.END, line.strip())
            history_listbox.bind('<Double-Button-1>', load_from_history)
            btn_clear_hist = tk.Button(h_win, text='Очистить историю', command=clear_txt_file)
            btn_clear_hist.pack(pady=(0, 10))
        except Exception as e:
            print(f'Ошибка истории: {e}')
            messagebox.showinfo('!', 'Пусто')

    # Добавление текста нажатой кнопки в поле ввода
    def on_click(text):
        if text in ('sin', 'cos', 'tan', 'log', 'ln', 'fact'):
            display.insert(tk.END, text + '(')
        else:
            display.insert(tk.END, text)

    # Полная очистка дисплея
    def clear(event=None):
        display.delete(0, tk.END)

    # Функции памяти
    def memory_clear():
        memory['val'] = 0.0

    def memory_recall():
        val = memory['val']
        if val.is_integer():
            val = int(val)
        display.insert(tk.END, str(val))

    def memory_add():
        calculate()
        try:
            memory['val'] += float(display.get())
        except ValueError:
            pass

    def memory_sub():
        calculate()
        try:
            memory['val'] -= float(display.get())
        except ValueError:
            pass

    def toggle_theme():
        nonlocal is_dark_theme
        is_dark_theme = not is_dark_theme
        theme = THEME_DARK if is_dark_theme else THEME_LIGHT

        window.configure(bg=theme['bg'])
        display.configure(bg=theme['disp'], fg=theme['text'])
        preview_label.configure(bg=theme['bg'])

        for widget in window.winfo_children():
            if isinstance(widget, Button):
                text = widget.cget('text')
                if text == '🌙':
                    widget.configure(text='☀️', bg=theme['spec'])
                elif text == '☀️':
                    widget.configure(text='🌙', bg=theme['spec'])
                elif text in ['/', '*', '-', '+', '=']:
                    widget.configure(bg=theme['op'])
                elif text in ['√', 'ˆ', 'π', '(', ')', 'sin', 'cos', 'tan', 'fact', 'log', 'ln', '%']:
                    widget.configure(bg=theme['math'])
                elif text in ['C', 'DEL', 'H', 'MC', 'MR', 'M+', 'M-', '+/-']:
                    widget.configure(bg=theme['spec'])
                else:
                    widget.configure(bg=theme['num'])
    # Смена знака
    def change_sign():
        current = display.get()
        if current.startswith('-'):
            display.delete(0, 1)
        else:
            display.insert(0, '-')

    def update_preview(*args):
        expression = dislpay_var.get()
        if not expression:
            preview_label.config(text='')
            return

        temp_expr = expression
        open_b = temp_expr.count('(')
        close_b = temp_expr.count(')')

        if open_b > close_b:
            temp_expr += ')' * (open_b - close_b)

        temp_expr = temp_expr.replace('√', 'math.sqrt(')
        temp_expr = temp_expr.replace('ˆ', '**').replace('^', '**')
        temp_expr = temp_expr.replace('π', str(math.pi))
        temp_expr = temp_expr.replace('sin', 'math.sin')
        temp_expr = temp_expr.replace('cos', 'math.cos')
        temp_expr = temp_expr.replace('tan', 'math.tan')
        temp_expr = temp_expr.replace('fact', 'math.factorial')
        temp_expr = temp_expr.replace('log', 'math.log10')
        temp_expr = temp_expr.replace('ln', 'math.log')
        temp_expr = temp_expr.replace('%', '/100')

        try:
            result = eval(temp_expr)
            preview_label.config(text=f'{result}')
        except Exception:
            preview_label.config(text='')
    dislpay_var.trace_add('write', update_preview)

    # Вычисление
    def calculate(event=None):
        expression = display.get()
        if not expression: return

        open_brackets = expression.count('(')
        close_breackets = expression.count(')')

        if open_brackets > close_breackets:
            expression += ')' * (open_brackets - close_breackets)
            display.delete(0, tk.END)
            display.insert(0, expression)

        try:
            temp_expression = expression.replace('√', 'math.sqrt(')
            temp_expression = temp_expression.replace('ˆ', '**').replace('^', '**')
            temp_expression = temp_expression.replace('π', str(math.pi))
            temp_expression = temp_expression.replace('sin', 'math.sin')
            temp_expression = temp_expression.replace('cos', 'math.cos')
            temp_expression = temp_expression.replace('tan', 'math.tan')
            temp_expression = temp_expression.replace('fact', 'math.factorial')
            temp_expression = temp_expression.replace('log', 'math.log10')
            temp_expression = temp_expression.replace('ln', 'math.log')
            temp_expression = temp_expression.replace('%', '/100')

            result = eval(temp_expression)

            display.delete(0, tk.END)
            display.insert(0, str(result))

            try:
                save_to_file(expression, result)
            except Exception as file_err:
                print(f'Ошибка вычисления: {file_err}')

        except Exception as calc_err:
            print(f'Ошибка вычисления: {calc_err}')
            display.delete(0, tk.END)
            display.insert(0, 'Ошибка')

    # Дисплей
    preview_label = tk.Label(window, text='', font=('Arial', 14), bg=COLOR_BG, fg=COLOR_BTN_SPEC, anchor='e')
    preview_label.grid(row=0, column=0, columnspan=4, sticky='nsew', padx=10, pady=(15, 0))
    display = tk.Entry(window, font=('Arial', 28), borderwidth=0, textvariable=dislpay_var, bg=COLOR_DISPLAY, fg=COLOR_TEXT, justify='right')
    display.grid(row=1, column=0, columnspan=4, padx=10, pady=(5, 20), sticky='nsew')
    display.focus_set()

    # Бинды
    window.bind('<Return>', calculate)
    window.bind('<KP_Enter>', calculate)
    window.bind('<Escape>', clear)

    # Кнопки
    buttons = [
        ('MC', COLOR_BTN_SPEC), ('MR', COLOR_BTN_SPEC), ('M+', COLOR_BTN_SPEC), ('M-', COLOR_BTN_SPEC),
        ('sin', COLOR_BTN_MATH), ('cos', COLOR_BTN_MATH), ('tan', COLOR_BTN_MATH), ('fact', COLOR_BTN_MATH),
        ('log', COLOR_BTN_MATH), ('ln', COLOR_BTN_MATH), ('+/-', COLOR_BTN_SPEC), ('%', COLOR_BTN_MATH),
        ('√', COLOR_BTN_MATH), ('ˆ', COLOR_BTN_MATH), ('π', COLOR_BTN_MATH), ('DEL', COLOR_BTN_SPEC),
        ('(', COLOR_BTN_MATH), (')', COLOR_BTN_MATH), ('C', COLOR_BTN_SPEC), ('/', COLOR_BTN_OP),
        ('7', COLOR_BTN_NUM), ('8', COLOR_BTN_NUM), ('9', COLOR_BTN_NUM), ('*', COLOR_BTN_OP),
        ('4', COLOR_BTN_NUM), ('5', COLOR_BTN_NUM), ('6', COLOR_BTN_NUM), ('-', COLOR_BTN_OP),
        ('1', COLOR_BTN_NUM), ('2', COLOR_BTN_NUM), ('3', COLOR_BTN_NUM), ('+', COLOR_BTN_OP),
        ('H', COLOR_BTN_SPEC), ('0', COLOR_BTN_NUM), ('.', COLOR_BTN_NUM), ('🌙', COLOR_BTN_SPEC)
    ]

    # Удаление последнего символа
    def delete_last():
        current = display.get()
        display.delete(0, tk.END)
        display.insert(0, current[:-1])

    # Генерация кнопок
    row_val = 2
    col_val = 0
    for text, color in buttons:
        if text == '=':
            action = calculate
        elif text == 'C':
            action = clear
        elif text == 'H':
            action = show_history
        elif text == 'DEL':
            action = delete_last
        elif text == 'MC':
            action = memory_clear
        elif text == 'MR':
            action = memory_recall
        elif text == 'M+':
            action = memory_add
        elif text == 'M-':
            action = memory_sub
        elif text == '🌙':
            action = toggle_theme
        elif text == '+/-':
            action = change_sign
        else:
            action = lambda t=text: on_click(t)
            
        btn = Button(window, text=text, font=('Arial', 14, 'bold'), bg=color, fg='black', command=action,
                        relief='flat', width=5, height=2)
        btn.grid(row=row_val, column=col_val, padx=5, pady=5, sticky='nsew')

        col_val += 1
        if col_val > 3:
            col_val = 0
            row_val += 1

    btn_equal = Button(window, text='=', font=('Arial', 14, 'bold'), bg=COLOR_BTN_OP, fg='black', command=calculate, relief='flat', height=2)
    btn_equal.grid(row=11, column=0, columnspan=4, padx=2, pady=2, sticky='nsew')

    # Настройка строк и колонок
    for i in range(4):
        window.grid_columnconfigure(i, weight=1)
    for i in range(1, 12):
        window.grid_rowconfigure(i, weight=1)

    # Запуск бесконечного главного цикла (безумие)
    window.mainloop()

if __name__ == '__main__':
    start_calculator()