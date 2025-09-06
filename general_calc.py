from tkinter import *
from tkinter import messagebox

# Константы (poor man's config)
WINDOW_TITLE = "Калькулятор"
WINDOW_SIZE = '500x500'
INPUT_LABEL = "Ввод выражения"
RESULT_WINDOW_TITLE = "Результат вычисления"

# Переменные
input_stack = [] # Стек в обратной польской нотации

def show_result(result):
    messagebox.showinfo(RESULT_WINDOW_TITLE, result)

# Основная функция расчета
def calculate():
    for i in range(len(input_stack)):
        elem = input_stack[i]
        # Если elem число - скип, если операция - работаем
        try:
            number = int(elem)
            continue
        except:
            result = int(input_stack[i-1]) + int(input_stack[i-2])
    show_result(result)

def put_in_stack(element):
    input_stack.append(element)

# Функция по клику на любую кнопку
def button_click(text, row, col):
    if (text == "="):
        calculate()
    elif (text == ""):
        pass
    else:
        put_in_stack(text)
    return

# Функция создания кнопок 
def create_button(text, row, col):
    button = Button(window, text=text, command= lambda: button_click(text, row, col), width=5, height=2)
    button.grid(row=row, column=col, padx=5, pady=5)
    return button

# Создание окна приложения
window = Tk()
window.title(WINDOW_TITLE)
window.geometry(WINDOW_SIZE)
window.resizable(False, False)

buttons = [
    ["Del", "(", ")", "*"],
    ["7", "8", "9", "/"],
    ["4", "5", "6", "-"],
    ["1", "2", "3", "+"],
    ["C", "0", "=", "|x|"],
    ["log_e(x)", "e^x", "x^2", "sqrt(x)"],
    ["sin(x)", "cos(x)", "tan(x)", "ctan(x)"]
]

for row in range(len(buttons)):
    for col in range(len(buttons[row])):
        button = create_button(buttons[row][col], row, col)

# Поля ввода
input_label = Label(window, text=INPUT_LABEL)
input_label.grid(row=0, column=4)

input_entry = Entry(window, width=40)
input_entry.grid(row=1, column=4)

# Вечный цикл отрисовки
window.mainloop()