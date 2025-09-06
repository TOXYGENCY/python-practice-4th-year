import tkinter as tk
from tkinter import messagebox

# Константы (poor man's config)
WINDOW_TITLE = "Калькулятор ИМТ"
WINDOW_SIZE = '220x150'
HEIGHT_LABEL = "Введите рост (в см)."
WEIGHT_LABEL = "Введите вес (в кг)."
SUBMIT_LABEL = "Рассчитать"
RESULT_WINDOW_TITLE = "Результат"
RESULT_BELOW_NORM = "Недостаточная масса тела."
RESULT_NORM = "Соответствует норме массы тела."
RESULT_ABOVE_NORM = "Соответствует избыточной массе тела."
RESULT_ABOVE_NORM_2 = "Соответствует ожирению."
ERROR_MESSAGE = "Возникла ошибка. Допустимы только числовые значения"
ERROR_WINDOW_TITLE = "Ошибка"

# Функция показа окна с результатом расчета 
def show_result_message(bmi):
    if (bmi < 18.5):
        messagebox.showinfo(RESULT_WINDOW_TITLE, f"ИМТ = {bmi}. {RESULT_BELOW_NORM}")
    elif (bmi > 18.5) and (bmi < 24.9):
        messagebox.showinfo(RESULT_WINDOW_TITLE, f"ИМТ = {bmi}. {RESULT_NORM}")
    elif (bmi > 24.9) and (bmi < 29.9):
        messagebox.showinfo(RESULT_WINDOW_TITLE, f"ИМТ = {bmi}. {RESULT_ABOVE_NORM}")
    else:
        messagebox.showinfo(RESULT_WINDOW_TITLE, f"ИМТ = {bmi}. {RESULT_ABOVE_NORM_2}")

# Функция рассчета ИМТ
def calculate_bmi():
    try: # Обработка ошибки данных
        height = int(height_entry.get()) / 100 # Перевод в метры
        weight = int(weight_entry.get())
    except:
        messagebox.showerror(ERROR_WINDOW_TITLE, ERROR_MESSAGE)
    bmi = weight/(height**2)
    bmi = round(bmi, 1)
    show_result_message(bmi)
    print("BMI =", bmi)

# Создание окна приложения
window = tk.Tk()
window.title(WINDOW_TITLE)
window.geometry(WINDOW_SIZE)
window.resizable(False, False)

# Поля роста
height_label = tk.Label(window, text=HEIGHT_LABEL)
height_label.grid(row=0, column=3, padx=50)

height_entry = tk.Entry(window)
height_entry.grid(row=1, column=3, padx=50)

# Поля веса
weight_label = tk.Label(window, text=WEIGHT_LABEL)
weight_label.grid(row=3, column=3, padx=50)

weight_entry = tk.Entry(window)
weight_entry.grid(row=4, column=3, padx=50)

# Кнопка ввода
submit_button = tk.Button(window, text=SUBMIT_LABEL, command=calculate_bmi)
submit_button.grid(row=5, column=3, padx=50, pady=15)

# Вечный цикл отрисовки
window.mainloop()