from tkinter import *
from tkinter import messagebox

# Константы (poor man's config)
WINDOW_TITLE = "Калькулятор"
WINDOW_SIZE = "800x640"
INPUT_LABEL = "Ввод выражения"
RESULT_WINDOW_TITLE = "Результат вычисления"
VALIDATION_ERROR_TITLE = "Ошибка ввода"


# Переменные
num_buffer = ""  # Буфер для учета многозначных чисел
notation = []  # Стек с обратной польской нотацией
operator_stack = []  # Стек с операторами
operators = {  # словарь операторов и их приоритетов
    "*": 1,
    "/": 1,
    "+": 0,
    "-": 0,
}
operations = {  # словарь операций и их приоритетов
    "**": 1,
    "e^": 1,
    "sqrt": 1,
    "log_e": 0,
    "sin": 0,
    "cos": 0,
    "tan": 0,
    "ctan": 0,
}

# Проверяет является ли X числом
def is_int(x):
    try:
        int(x)
        return True
    except:
        return False


# Сохранение числа из накоплений буфера и его очистка
def save_number():
    global num_buffer, notation

    if len(num_buffer) > 0:
        notation.append(int(num_buffer))
    num_buffer = ""
    print("Number saved. Buffer cleared.")


# Основная функция парсинга инфиксной записи в ОПН
def parse_input():
    global num_buffer, operator_stack, operators, notation
    # Очищаем рабочие переменные
    notation, operator_stack, num_buffer = [], [], ""

    input = input_entry.get()
    print("Processing:", input)
    for i in range(len(input)):
        symb = input[i]

        # Числа добавляем в буфер
        if is_int(symb):
            num_buffer += symb
            # Если это последняя цифра, то сохраняем число
            if i == len(input) - 1:
                save_number()

        # Откр. скобка в стек
        elif symb == "(":
            save_number()
            operator_stack.append(symb)

        # Добавляем операции в стек
        elif i != len(input) and str(symb + input[i + 1]) in operations:
            save_number()
            operator_stack.append(symb)

        # Добавляем операторы в стек в порядке приоритетов
        elif symb in operators:
            save_number()
            oper = symb
            # Пока видим операторы в высшим приоритетом - переносим их в нотацию
            while (
                len(operator_stack) > 0
                and operator_stack[-1] != "("  # вытаскиваем до откр. скобки
                and operators[oper] <= operators[operator_stack[-1]]
            ):
                notation.append(operator_stack.pop())
            operator_stack.append(symb)

        # По закрытии скобок переносим в нотацию все внутренние (упорядоченные) операторы
        elif symb == ")":
            save_number()
            while len(operator_stack) > 0 and operator_stack[-1] != "(":
                notation.append(operator_stack.pop())
            operator_stack.pop()  # удаление оставшейся открывающей скобки

        # Любой другой случай
        else:
            save_number()
            print("unusued else triggered, symb is", symb)

    # После полного прохода по инфиксному вводу добавляем остатки (упорядоченных) операторов в нотацию
    while len(operator_stack) > 0:
        notation.append(operator_stack.pop())

    print("Parsing done:")
    print("- Notation is", notation)
    print("- Operator_stack is", operator_stack)


def perform_operation(a, b, operation):
    if operation == "+":
        return a + b
    elif operation == "-":
        return a - b
    elif operation == "*":
        return a * b
    elif operation == "/":
        return int(a / b)


def calculate_notation():
    global notation
    calc_stack = []  # стек вычислений выражения

    for elem in notation:
        if is_int(elem):
            calc_stack.append(elem)

        elif elem in operators:
            b = calc_stack.pop()
            a = calc_stack.pop()
            result = perform_operation(a, b, elem)
            calc_stack.append(result)

    return calc_stack.pop()


# Функция, запускающая процесс вычисления
def calculate():
    parse_input()  # делаем нотацию
    result = str(int(calculate_notation()))
    messagebox.showinfo(RESULT_WINDOW_TITLE, result)


# Функция с валидациями ввода. Возвращает кортеж из результата и сообщения ошибки
def validate_input():
    if input_entry.get().count("(") != input_entry.get().count(")"):
        return (False, "Перепроверьте все ли скобки закрыты/открыты.")
    return (True, "")


# Общая функция клика для всех созданных кнопок
def button_click(text, value):
    if text == "=":
        (valid, err_message) = validate_input()
        if valid:
            calculate()
        else:
            messagebox.showerror(VALIDATION_ERROR_TITLE, err_message)

    # Очистка поля ввода
    elif value == "C":
        input_entry.delete(0, "end")

    # Стереть последний знак
    elif value == "D":
        input_entry.delete(len(input_entry.get()) - 1, "end")

    else:
        # Запись текста с кнопки в строку
        input_entry.insert(len(input_entry.get()), text)


# Функция создания кнопок
def create_button(text, value, row, col):
    button = Button(
        window,
        text=text,
        command=lambda: button_click(text, value),
        width=5,
        height=2,
        font=("Arial", 16),
    )
    button.grid(row=row, column=col, padx=5, pady=5)
    return button


# Создание окна приложения
window = Tk()
window.title(WINDOW_TITLE)
window.geometry(WINDOW_SIZE)
window.resizable(False, False)


# Все ("названия":"внутренние_значения") кнопок. Для каждой создается отдельная кнопка
# При парсинге изначальной строки названия будут заменяться на внутренние_значения
# Внутренние значения нужны для простого парсинга операций по двум знакам
button_labels = [
    [("Del", "D"), ("(", "("), (")", ")"), ("*", "*")],
    [("7", "7"), ("8", "8"), ("9", "9"), ("/", "/")],
    [("4", "4"), ("5", "5"), ("6", "6"), ("-", "-")],
    [("1", "1"), ("2", "2"), ("3", "3"), ("+", "+")],
    [("C", "C"), ("0", "0"), ("=", "="), ("|x|", "||")],
    [("log_e(x)", "le"), ("e^", "e^"), ("**", "**"), ("sqrt", "sq")],
    [("sin", "sn"), ("cos", "cs"), ("tan", "tn"), ("ctan", "ct")],
]


# Цикл создания кнопок
for row in range(len(button_labels)):
    for col in range(len(button_labels[row])):
        button = create_button(
            button_labels[row][col][0], button_labels[row][col][1], row, col
        )


# Поля ввода
input_label = Label(window, text=INPUT_LABEL, font=("Arial", 16))
input_label.grid(row=0, column=4)

input_entry = Entry(window, width=40, font=("Arial", 14))
input_entry.grid(row=1, column=4)


# Вечный цикл отрисовки
window.mainloop()
