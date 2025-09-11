from tkinter import *
from tkinter import messagebox
from math import log, sin, cos, tan, radians

# Константы (poor man's config)
WINDOW_TITLE = "Калькулятор"
WINDOW_SIZE = "800x640"
INPUT_LABEL = "Ввод выражения"
RESULT_WINDOW_TITLE = "Результат вычисления"
VALIDATION_ERROR_TITLE = "Ошибка ввода"


# Переменные

# Все ("названия":"внутренние_значения") кнопок. Для каждой создается отдельная кнопка
# При парсинге изначальной строки названия будут заменяться на внутренние_значения
# Внутренние значения нужны для простого парсинга операций по двум знакам
button_labels = [
    [("Del", "D"), ("(", "("), (")", ")"), ("*", "*")],
    [("7", "7"), ("8", "8"), ("9", "9"), ("/", "/")],
    [("4", "4"), ("5", "5"), ("6", "6"), ("-", "-")],
    [("1", "1"), ("2", "2"), ("3", "3"), ("+", "+")],
    [("C", "C"), ("0", "0"), ("=", "="), ("|x|", "|")],
    [("log_e(x)", "ln"), ("^", "^"), ("sqrt(x)", "sq"), ("=", "=")],
    [("sin(x)", "sn"), ("cos(x)", "cs"), ("tan(x)", "tn"), ("ctan(x)", "ct")],
]
num_buffer = ""  # Буфер для учета многозначных чисел
notation = []  # Стек с обратной польской нотацией
operation_stack = []  # Стек с операторами
operations = {  # словарь операций и их приоритетов
    "--": 3,  # Явный унарный минус
    "^": 2,
    "sq": 2,  # sqrt
    "ln": 1,  # log_e
    "sn": 1,  # sin
    "cs": 1,  # cos
    "tn": 1,  # tan
    "ct": 1,  # ctan
    "*": 1,
    "/": 1,
    "+": 0,
    "-": 0,
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


# Конвертация строки ввода в укороченный стандартизированный вид перед обработкой
def convert_symbols(text):
    text = str(text).replace("x", "1", -1)  # допущение
    text = str(text).replace("**", "^", -1)
    text = str(text).replace("sqrt", "sq", -1)
    text = str(text).replace("log_e", "ln", -1)
    text = str(text).replace("sin", "sn", -1)
    text = str(text).replace("cos", "cs", -1)
    text = str(text).replace("tan", "tn", -1)
    text = str(text).replace("ctan", "ct", -1)
    text = str(text).replace(" ", "", -1)
    return text


# Cокращение проверки на спец символ для условий в parse_input()
def is_special(current, last):
    current = str(current)
    last = str(last)
    is_oper = str(current + last) in operations
    is_bracket = str(current + last) in ["(", ")", "|"]
    return is_oper or is_bracket


# Основная функция парсинга инфиксной записи в ОПН
def parse_input():
    global num_buffer, operation_stack, operations, notation
    # Очищаем рабочие переменные
    notation, operation_stack, num_buffer = [], [], ""

    input = convert_symbols(input_entry.get())

    print("Processing:", input)
    i = 0
    # Из-за изменения строки input, нельзя использовать фиксированный for
    while i < len(input):
        symb = input[i]
        print("--processing:", symb)

        # Числа добавляем в буфер
        if is_int(symb):
            num_buffer += symb
            # Если это последняя цифра, то сохраняем число
            if i == len(input) - 1:
                save_number()

        # Унарный минус. Либо по контексту, либо явный "--"
        elif (
            ((i < len(input) - 1) and (symb == "-" == str(symb + input[i + 1])))
            or ((i == 0) and (symb == "-"))
            or (
                (0 < i < len(input) - 1)
                and (symb == "-")
                and (is_special(symb, input[i - 1]))
            )
        ):
            save_number()
            # Извращение чтобы задублировать унарный минус из "-" в явный "--"
            # вставка доп "-" в разрыве
            # input = input[0:i:1] + "-" + input[i + 1 : -1 : 1]
            operation_stack.append("--")

        # Откр. скобка в стек
        elif symb == "(":
            save_number()
            operation_stack.append(symb)

        # Добавляем операции в стек. Проверяем по двум символам
        elif i < len(input) - 1 and str(symb + input[i + 1]) in operations:
            save_number()
            operation_stack.append(str(symb + input[i + 1]))

        # Добавляем операторы в стек в порядке приоритетов
        elif symb in operations:
            save_number()
            oper = symb
            # Пока видим операторы в высшим приоритетом - переносим их в нотацию
            while (
                len(operation_stack) > 0
                and operation_stack[-1] != "("  # вытаскиваем до откр. скобки
                and operations[oper] <= operations[operation_stack[-1]]
            ):
                notation.append(operation_stack.pop())
            operation_stack.append(symb)

        # По закрытии скобок переносим в нотацию все внутренние (упорядоченные) операторы
        elif symb == ")":
            save_number()
            while len(operation_stack) > 0 and operation_stack[-1] != "(":
                notation.append(operation_stack.pop())
            operation_stack.pop()  # удаление оставшейся открывающей скобки

        # Любой другой случай
        else:
            save_number()
            print("skipping symb", symb)
        i += 1

    # После полного прохода по инфиксному вводу добавляем остатки (упорядоченных) операторов в нотацию
    while len(operation_stack) > 0:
        notation.append(operation_stack.pop())

    print("Parsing done:")
    print("- Notation is", notation)
    print("- Operator_stack is", operation_stack)

# Выполнение операции над одним/двумя операндами (как же хочется eval или хотя бы switch-case...)
def perform_operation(a, b, operation):
    print(f"...calculating {a} {operation} {b}")
    if operation == "+":
        return a + b
    elif operation == "-":
        return a - b
    elif operation == "*":
        return a * b
    elif operation == "/":
        return a / b
    elif operation == "^":
        return a**b
    elif operation == "--":
        return a * -1
    elif operation == "sq":
        return a**0.5
    elif operation == "ln":
        return log(radians(a))
    elif operation == "sn":
        return sin(radians(a))
    elif operation == "cs":
        return cos(radians(a))
    elif operation == "tn":
        return tan(radians(a))
    elif operation == "ct":
        return cos(radians(a)) / sin(radians(a))


def calculate_notation():
    global notation
    calc_stack = []  # стек вычислений выражения

    for elem in notation:
        a = 0
        b = 0

        if is_int(elem):
            calc_stack.append(elem)

        # Для бинарных операций
        elif elem in ["*", "^", "/", "+", "-"]:
            b = calc_stack.pop()
            a = calc_stack.pop()
            result = perform_operation(a, b, elem)
            calc_stack.append(result)

        # Для унарных операций
        elif elem in ["--", "sq", "ln", "sn", "cs", "tn", "ct"]:
            a = calc_stack.pop()
            result = perform_operation(a, 0, elem)
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

# TODO: добавить временный буфер для операций таких как sq, чтобы сначала класть скобки и то что в них, а потом саму операцию
# TODO: пофиксить унарный минус
