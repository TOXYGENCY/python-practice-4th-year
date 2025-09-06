from tkinter import *

# Константы (poor man's config)
WINDOW_TITLE = "Калькулятор"
WINDOW_SIZE = '500x500'
INPUT_LABEL = "Ввод выражения"

# Основная функция расчета
def calculate():
    print("TODO")

# Функция по клику на любую кнопку
def button_click(text, row, col):
    if (text == "="):
        calculate()
    elif (text == ""):
        pass
    else:
        input_entry.insert(len(input_entry.get()), text)
    return

# Функция создания кнопок 
def create_button(text, row, col):
    button = Button(window, text=text, command= lambda: button_click(text, row, col))
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
    ["C", "0", "=", "sqrt(x)"],
    ["log_e(x)", "e^x", "|x|", "rad(x)"],
    ["sin(x)", "cos(x)", "tan(x)", "ctan(x)"]
]

for row in range(len(buttons)):
    for col in range(len(buttons[row])):
        button = create_button(buttons[row][col], row, col)

# Поля ввода
input_label = Label(window, text=INPUT_LABEL)
input_label.grid(row=10, column=4, padx=50)

input_entry = Entry(window)
input_entry.grid(row=11, column=4, padx=50)

# Вечный цикл отрисовки
window.mainloop()