from tkinter import *
from tkinter import messagebox
from math import e, log, sin, cos, tan, radians

# Константы (poor man's config)
WINDOW_TITLE = "Калькулятор"
WINDOW_SIZE = "320x600"
INPUT_LABEL = "Ввод выражения"
RESULT_WINDOW_TITLE = "Результат вычисления"
VALIDATION_ERROR_TITLE = "Ошибка ввода"
CALC_ERROR_TITLE = "Ошибка вычисления"
CALC_ERROR_TEXT = "Во время вычислений произошла ошибка"
OPERATIONS = {  # словарь операций и их приоритетов
    "--": 3,  # Явный унарный минус
    "abs": 2,  # модуль
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
# Все ("названия":"внутренние_значения") кнопок. Для каждой создается отдельная кнопка
# При парсинге изначальной строки названия будут заменяться на внутренние_значения
# Внутренние значения нужны для простого парсинга операций по двум знакам
BUTTON_LABELS = [
    [("(", "("), (")", ")"), ("^", "^"), ("*", "*")],
    [("7", "7"), ("8", "8"), ("9", "9"), ("/", "/")],
    [("4", "4"), ("5", "5"), ("6", "6"), ("-", "-")],
    [("1", "1"), ("2", "2"), ("3", "3"), ("+", "+")],
    [("Del", "D"), ("0", "0"), ("=", "="), ("|", "|")],
    [("C", "C"), ("ln(x)", "ln"), ("=", "="), ("sqrt(x)", "sq")],
    [("sin(x)", "sn"), ("cos(x)", "cs"), ("tan(x)", "tn"), ("ctan(x)", "ct")],
]
BG_COLOR = "#e4eaec"
FG_COLOR = "black"
BG_COLOR_BUTTON = "#e2ecf1"
BG_COLOR_SPECIAL = "#d5b5b9"
FG_COLOR_SPECIAL = "#3B0009"
BG_COLOR_NUMBER = "#c5d3e0"
BG_COLOR_CALC = "#bbd6be"
FG_COLOR_ACTIVE = "cyan"
BG_COLOR_ACTIVE = "gray"

# Переменные
num_buffer = ""  # Буфер для учета многозначных чисел
notation = []  # Стек с обратной польской нотацией
operation_stack = []  # Стек с операторами


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


# Cокращение проверки предыдущ. на спец символ для условий в parse_input()
def is_special(last):
    global OPERATIONS

    last = str(last)
    is_oper = last in OPERATIONS and last != "-"
    is_bracket = last in ["(", ")", "|"]
    return is_oper or is_bracket


# Основная функция парсинга инфиксной записи в ОПН
def parse_input():
    global num_buffer, operation_stack, OPERATIONS, notation
    # Очищаем рабочие переменные
    notation, operation_stack, num_buffer = [], [], ""

    input = convert_symbols(input_entry.get())
    print("Processing:", input)
    i = 0
    abs_count = 0
    # Из-за изменения строки input, нельзя использовать фиксированный for
    while i < len(input):
        symb = input[i]

        # Числа добавляем в буфер
        if is_int(symb):
            num_buffer += symb
            # Если это последняя цифра, то сохраняем число
            if i == len(input) - 1:
                save_number()

        # Унарный минус. Либо по контексту, либо явный "--"
        elif (
            (  # Явно задан "--"
                (i < len(input) - 1) and (symb == "-" == str(symb + input[i + 1]))
            )
            or ((i == 0) and (symb == "-"))  # Неявный, но первый символ
            or (  # стоит после оператора
                (0 < i < len(input) - 1)
                and (symb == "-")
                and (is_special(input[i - 1]) and input[i - 1] != ")")
            )
        ):
            save_number()
            operation_stack.append("--")

        # Откр. скобка в стек
        elif symb == "(":
            save_number()
            operation_stack.append(symb)

        # Четный (откр.) знак модуля в стек
        elif symb == "|" and abs_count % 2 == 0:
            save_number()
            abs_count += 1
            operation_stack.append(symb)

        # Добавляем операции в стек. Проверяем по двум символам
        elif i < len(input) - 1 and str(symb + input[i + 1]) in OPERATIONS:
            save_number()
            operation_stack.append(str(symb + input[i + 1]))

        # Добавляем операторы в стек в порядке приоритетов
        elif symb in OPERATIONS:
            save_number()
            oper = symb
            # Пока видим операторы в высшим приоритетом - переносим их в нотацию
            while (
                len(operation_stack) > 0
                and operation_stack[-1] != "("
                and operation_stack[-1] != "|"  # вытаскиваем до откр. скобки или модуля
                and OPERATIONS[oper] <= OPERATIONS[operation_stack[-1]]  # приоритеты
            ):
                notation.append(operation_stack.pop())
            operation_stack.append(symb)

        # По закрытии модуля переносим в нотацию все внутренние (упорядоченные) операторы
        elif symb == "|" and abs_count % 2 != 0:
            save_number()
            abs_count += 1
            while len(operation_stack) > 0 and operation_stack[-1] != "|":
                notation.append(operation_stack.pop())
            notation.append(
                "abs"
            )  # добавление операции модуля в нотацию сразу после остальных
            operation_stack.pop()  # удаление оставшегося открывающего модуля

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
    elif operation == "abs":
        return abs(a)
    elif operation == "sq":
        return a**0.5
    elif operation == "ln":
        return log(a)
    elif operation == "sn":
        return sin(radians(a))
    elif operation == "cs":
        return cos(radians(a))
    elif operation == "tn":
        return tan(radians(a))
    elif operation == "ct":
        return 1 / tan(radians(a))

# Пошаговое вычисление готовой ОПН
def calculate_notation():
    global notation
    calc_stack = []  # стек вычислений выражения

    i = 0
    while i <= len(notation) - 1:
        elem = notation[i]
        print("---processing", elem, calc_stack)
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
        elif elem in ["--", "sq", "ln", "sn", "cs", "tn", "ct", "abs"]:
            a = calc_stack.pop()
            result = perform_operation(a, "none", elem)
            calc_stack.append(result)

        i += 1

    return calc_stack.pop()


# Функция, запускающая процесс вычисления
def calculate():
    parse_input()  # делаем нотацию
    try:
        result = str(calculate_notation())
        messagebox.showinfo(RESULT_WINDOW_TITLE, result)
    except Exception as ex:
        messagebox.showerror(CALC_ERROR_TITLE, CALC_ERROR_TEXT)
        raise ex


# Функция с валидациями ввода. Возвращает кортеж из результата и сообщения ошибки
def validate_input():
    input = input_entry.get()
    if input.count("(") != input.count(")"):
        return (False, "Перепроверьте все ли скобки закрыты/открыты.")
    elif input.count("|") % 2 != 0:
        return (False, "Перепроверьте все ли модули закрыты.")
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
    bg_color = BG_COLOR_BUTTON
    fg_color = FG_COLOR

    if value in ["C", "D"]:
        bg_color = BG_COLOR_SPECIAL
        fg_color = FG_COLOR_SPECIAL
    elif is_int(value):
        bg_color = BG_COLOR_NUMBER
    elif value == "=":
        bg_color = BG_COLOR_CALC

    button = Button(
        window,
        text=text,
        command=lambda: button_click(text, value),
        width=5,
        height=2,
        font=("Arial", 16),
        activeforeground=FG_COLOR_ACTIVE,
        activebackground=BG_COLOR_ACTIVE,
        cursor="hand2",
        background=bg_color,
        foreground=fg_color,
    )
    button.grid(row=row, column=col, padx=4, pady=4)
    return button


# Создание окна приложения
window = Tk()
window.title(WINDOW_TITLE)
window.geometry(WINDOW_SIZE)
window.resizable(False, False)
window.configure(background=BG_COLOR)

# Цикл создания кнопок
column_offset = 0
row_offset = 2
for row in range(len(BUTTON_LABELS)):
    for col in range(len(BUTTON_LABELS[row])):
        button = create_button(
            BUTTON_LABELS[row][col][0],
            BUTTON_LABELS[row][col][1],
            row + row_offset,
            col + column_offset,
        )


# Поля ввода
input_label = Label(window, text=INPUT_LABEL, font=("Arial", 14), background=BG_COLOR)
input_label.grid(row=0, column=0, columnspan=4, padx=5)

input_entry = Entry(window, width=27, font=("Arial", 14))
input_entry.grid(row=1, column=0, columnspan=4, pady=8)

# Вечный цикл отрисовки
window.mainloop()
